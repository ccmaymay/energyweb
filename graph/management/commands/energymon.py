#!/usr/bin/env python


'''
Connect to an energy monitoring device as those designed by Joseph
King of Rhizome Systems.  (These devices speak in TCP/IP and can
accept only one connection at a time.  They emit 45 bytes of data
about once every 10 seconds.)  Interpret the data, process it for
easier retrieval later (storage is cheap), and wait for the next
45-byte message.  (Loop endlessly unless interrupted.)  Called with
two arguments:  The sensor ID (as represented in the PostgreSQL DB)
and a command (start, stop, restart).  Daemonize on initialization.
'''


import socket, psycopg2, datetime, os.path, time, atexit, signal, sys
from django.core.management.base import BaseCommand, CommandError
from binascii import hexlify
from energyweb.graph.daemon import Daemon
from django.conf import settings
from logging import error, info, debug, basicConfig
from energyweb.graph.models import Sensor, PowerAverage, SensorReading
from django.db.models import Avg, Max, Min, Count
from django.db import connection, transaction


def rollback_on_exception(f):
    '''
    Catch any exception, rollback the transaction, then re-raise the
    exception.
    '''
    def _f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            transaction.rollback()
            raise
    return _f


class EnergyMonDaemon(Daemon):
    '''
    Subclass of a daemonizing class.  When initialized, wait for
    messages from a certain energy monitoring device, as described
    above.  (The particular device is given by the sensor_id argument
    to run() and is assumed to be represented in the database.) Insert
    data when it's received, and then wait for another message.
    '''

    def cleanup(self):
        '''
        Close database and socket connections in preparation for
        termination.
        '''
        info('Cleaning up: rolling back, disconnecting, disconnecting.')
        transaction.rollback()
        if hasattr(self, 'sock'):
            self.sock.close()

    def handle_signal(self, signum, frame):
        '''
        If a SIGQUIT, SIGTERM, or SIGINT is received, shutdown cleanly.
        '''
        if signum == signal.SIGQUIT:
            info('Caught SIGQUIT.')
        elif signum == signal.SIGTERM:
            info('Caught SIGTERM.')
        elif signum == signal.SIGINT:
            info('Caught SIGINT.')
        # cleanup() will be called since it is registered with atexit
        sys.exit(0)

    def open_socket(self):
        '''
        Open a socket to the device, looping until success.
        '''
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.sensor.ip, self.sensor.port))
                info('Socket connected to %s:%d.' 
                     % (self.sensor.ip, self.sensor.port))
                break
            except socket.error, detail:
                error(str(detail))
                error('Socket error.')
                error('Pausing, reopening socket.')
                time.sleep(settings.ERROR_PAUSE)

    def init_power_averages(self):
        self.power_averages = {}
        power_average_qs = PowerAverage.objects.filter(
            sensor=self.sensor).order_by('-trunc_reading_time')
        sensor_reading_qs = SensorReading.objects.filter(
            sensor=self.sensor).order_by('-reading_time')
        try:
            latest_reading = sensor_reading_qs.latest('reading_time')
        except SensorReading.DoesNotExist:
            for average_type in PowerAverage.AVERAGE_TYPES:
                self.power_averages[average_type] = None
        else:
            for average_type in PowerAverage.AVERAGE_TYPES:
                # Don't confuse trunc_latest_reading_time with the
                # similarly-named column of graph_poweraverage.
                # trunc_latest_reading_time is the truncated
                # reading_time of the latest row in graph_sensorreading
                # for this sensor.
                trunc_latest_reading_time = PowerAverage.date_trunc(
                    average_type, latest_reading.reading_time)

                try:
                    latest_average = power_average_qs.filter(
                        average_type=average_type).latest('trunc_reading_time')
                except PowerAverage.DoesNotExist:
                    latest_average = None

                if latest_average is None or (trunc_latest_reading_time 
                    > latest_average.trunc_reading_time):

                    aggr = sensor_reading_qs.filter(
                        reading_time__gte=trunc_latest_reading_time).aggregate(
                        awatthr=Avg('awatthr'),
                        bwatthr=Avg('bwatthr'),
                        cwatthr=Avg('cwatthr'),
                        num_points=Count('sensor'),
                        first_reading_time=Min('reading_time'),
                        last_reading_time=Max('reading_time'))
                    self.power_averages[average_type] = PowerAverage(
                        watts=(aggr['awatthr'] 
                               + aggr['bwatthr'] 
                               + aggr['cwatthr']),
                        num_points=aggr['num_points'],
                        average_type=average_type,
                        sensor=self.sensor,
                        first_reading_time=aggr['first_reading_time'],
                        last_reading_time=aggr['last_reading_time'],
                        trunc_reading_time=trunc_latest_reading_time)
                    self.power_averages[average_type].save()
                else:
                    self.power_averages[average_type] = latest_average

    @transaction.commit_manually
    @rollback_on_exception
    def run(self, sensor_id):
        '''
        Perform the main listen and insert loop of the program.
        (See file and class docstrings.)
        '''
        basicConfig(filename=(settings.MON_LOG_FILE_TEMPL % sensor_id),
                    format=settings.LOG_FORMAT, datefmt=settings.LOG_DATEFMT, 
                    level=settings.LOG_LEVEL)

        # Register exit and signal behaviors.
        atexit.register(self.cleanup)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGQUIT, self.handle_signal)

        self.sensor = Sensor.objects.get(pk=sensor_id)

        debug('Initializing power averages.')
        self.init_power_averages()
        transaction.commit()

        # If the sensor is three-phase, we want to add all three power
        # measurements to obtain the aggregate.  If the sensor is single
        # phase, only the first two measurements are meaningful---so 
        # we'll zero the third.
        factor = self.sensor.factor
        phase_factor = (self.sensor.three_phase and 1 or 0)
    
        self.open_socket()
    
        while True:
            data = ''
            debug('Listening for data.')
            # Loop until all 45 bytes of the message are collected.
            while len(data) < 45:
                data_recvd = self.sock.recv(1024)
                if data_recvd == '':
                    error('Socket died.  Printing data, closing, reopening.')
                    error(hexlify(data) + '.')
                    self.sock.close()
                    self.open_socket()
                    data = ''
                else:
                    data += data_recvd
            debug('Data received.  (45 bytes)')
            if data[0:4] != 'RTSD': # 52 54 53 44 in hex
                error('Bad data.  Printing data, closing socket, reopening.')
                error(hexlify(data) + '.')
                self.sock.close()
                self.open_socket()
            else:
                # If the rudimentary validation succeeded, proceed to
                # interpret the data for processing and storage.
                debug('Data validated.')
                d = {}
                d['rindex'] = ord(data[4])
                # Lots of little uints
                d['awatthr'] = factor * ((ord(data[5]) << 8) | ord(data[6]))
                d['bwatthr'] = factor * ((ord(data[7]) << 8) | ord(data[8]))
                d['cwatthr'] = factor * ((ord(data[9]) << 8) | ord(data[10]))
                d['avarhr'] = factor * ((ord(data[11]) << 8) | ord(data[12]))
                d['bvarhr'] = factor * ((ord(data[13]) << 8) | ord(data[14]))
                d['cvarhr'] = factor * ((ord(data[15]) << 8) | ord(data[16]))
                d['avahr'] = factor * ((ord(data[17]) << 8) | ord(data[18]))
                d['bvahr'] = factor * ((ord(data[19]) << 8) | ord(data[20]))
                d['cvahr'] = factor * ((ord(data[21]) << 8) | ord(data[22]))
                d['airms'] = factor * ((ord(data[23]) << 16) 
                                       | (ord(data[24]) << 8) 
                                       | ord(data[25]))
                d['birms'] = factor * ((ord(data[26]) << 16) 
                                       | (ord(data[27]) << 8) 
                                       | ord(data[28]))
                d['cirms'] = factor * ((ord(data[29]) << 16) 
                                       | (ord(data[30]) << 8) 
                                       | ord(data[31]))
                d['avrms'] = ((ord(data[32]) << 16) | (ord(data[33]) << 8) 
                                               | ord(data[34]))
                d['bvrms'] = ((ord(data[35]) << 16) | (ord(data[36]) << 8) 
                                               | ord(data[37]))
                d['cvrms'] = ((ord(data[38]) << 16) | (ord(data[39]) << 8) 
                                               | ord(data[40]))
                d['freq'] = ((ord(data[41]) << 8) | ord(data[42])) >> 4
                # for tempc:  at d['Amb'] = 25C, register = DF = Offset
                d['tempc'] = 25 + (ord(data[43]) - int('df', 16)) * 3

                reading_time = datetime.datetime.now()
                d['reading_time'] = reading_time
                d['sensor'] = self.sensor
    
                SensorReading.objects.create(**d)

                # Precompute averages (we have 10 seconds until the 
                # next message.
                watts = (d['awatthr'] + d['bwatthr'] 
                         + d['cwatthr'] * phase_factor)

                for average_type in PowerAverage.AVERAGE_TYPES:
                    trunc_reading_time = PowerAverage.date_trunc(average_type,
                        reading_time)
                    if (self.power_averages[average_type] is not None 
                        and trunc_reading_time == self.power_averages[
                                average_type].trunc_reading_time):

                        n = self.power_averages[average_type].num_points
                        self.power_averages[average_type].watts = (
                            (self.power_averages[average_type].watts * n 
                             + watts) 
                            / (n + 1))
                        self.power_averages[average_type].num_points = n + 1
                        self.power_averages[average_type].last_reading_time \
                            = reading_time
                    else:
                        if self.power_averages[average_type] is not None:
                            self.power_averages[average_type].save()
                        self.power_averages[average_type] = PowerAverage(
                            watts=watts,
                            num_points=1,
                            average_type=average_type,
                            sensor=self.sensor,
                            first_reading_time=reading_time,
                            last_reading_time=reading_time,
                            trunc_reading_time=trunc_reading_time)
                    self.power_averages[average_type].save()

                transaction.commit()
                debug('Data processed.')
    
        self.cleanup()
        info('Past main loop.  Exiting.')
        sys.exit(0)


class Command(BaseCommand):
    args = '<sensor_id> start|stop|restart'
    help = 'Monitor the specified Rhizome device.'

    def handle(self, *args, **options):
        if len(args) == 2:
            try:
                sensor_id = int(args[0])
            except ValueError:
                raise CommandError('Invalid sensor id: \'%s\'.' % args[0])
    
            daemon = EnergyMonDaemon(
                settings.MON_PID_FILE_TEMPL % sensor_id, args=(sensor_id,), 
                stdout=(settings.MON_LOG_FILE_TEMPL % sensor_id),
                stderr=(settings.MON_LOG_FILE_TEMPL % sensor_id))
            if args[1] == 'start':
                daemon.start()
            elif args[1] == 'stop':
                daemon.stop()
            elif args[1] == 'restart':
                daemon.restart()
            else:
                raise CommandError('Invalid action: \'%s\'.' % args[1])
        else:
            raise CommandError('Invalid number of arguments: %d.' % len(args))
