#!/usr/bin/env python


'''
Serve data on a TCP port (using the assumption that the machine can
listen on the specified address and port), imitating a Rhizome Systems 
energy monitoring device.  The imitation is accomplished by reading from
a "profile," i.e., a list of sample readings.  Called with two
arguments:  The sensor ID (as represented in the PostgreSQL DB)
and a command (start, stop, restart).  (The TCP port used will be that
specified in the database for the given sensor.)  Daemonize on 
initialization.
'''


import socket, psycopg2, datetime, atexit, signal, time, sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from energyweb.graph.daemon import Daemon
from logging import error, info, debug, basicConfig
from energyweb.graph.fake_rhizome_profiles import FAKE_RHIZOME_PROFILES
from SocketServer import TCPServer, BaseRequestHandler
from random import random, randint
from binascii import unhexlify
from energyweb.graph.models import Sensor


class FakeRhizomeHandler(BaseRequestHandler):
    '''
    Subclass of the SocketServer BaseRequestHandler that imitates a
    Rhizome device, as given by FakeRhizomeHandler.profile (assumed 
    to be set before connections are received).
    '''

    def handle(self):
        '''
        Imitate a Rhizome device by sending the data specified in
        self.profile.
        '''
        info('%s:%d connected.' % self.client_address)

        reading_num = 0
        reading = self.profile[reading_num]

        # Loop forever, sending every 10 seconds (roughly)
        while True:
            chars_sent = 0
            # Loop until a full reading (45 bytes) has been sent.
            while chars_sent < 45:
                chars_to_send = randint(1, 45 - chars_sent)
                r = reading[chars_sent:(chars_sent + chars_to_send)]
                self.request.send(r)
                chars_sent += chars_to_send
                debug('Reading %d: data sent.  (%d bytes)' 
                      % (reading_num, chars_to_send))

            reading_num += 1
            if reading_num == len(self.profile):
                reading_num = 0
            reading = self.profile[reading_num]

            time.sleep(10 + (random() - 0.5) * settings.FAKER_SLEEP_VARIATION)

        self.request.close()
        info('%s:%d closed.' % self.client_address)


class FakeRhizomeDaemon(Daemon):
    '''
    Subclass of a daemonizing class.  When initialized, wait for
    a connection on the TCP port specified in the database for the
    given energy monitoring device.  (The particular device is given 
    by the sensor_id argument to run().)  Send imitation data when a
    connection is received.
    '''

    def cleanup(self):
        '''
        Close database and socket connections in preparation for
        termination.
        '''
        info('Cleaning up: rolling back, disconnecting, disconnecting.')
        if hasattr(self, 'sock'):
            self.sock.shutdown()

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

    def run(self, sensor_id):
        '''
        Perform the main listen and send loop of the program.
        (See file and class docstrings.)
        '''
        basicConfig(filename=(settings.FAKER_LOG_FILE_TEMPL % sensor_id),
                    format=settings.LOG_FORMAT, datefmt=settings.LOG_DATEFMT, 
                    level=settings.LOG_LEVEL)

        # Register exit and signal behaviors.
        atexit.register(self.cleanup)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGQUIT, self.handle_signal)

        self.sensor = Sensor.objects.get(pk=sensor_id)
        addr = '%s:%d' % (self.sensor.ip, self.sensor.port)
        if self.sensor.name == '':
            desc = self.sensor.sensor_group.name
        else:
            desc = '%s %s' % (self.sensor.sensor_group.name, self.sensor.name)
    
        # TODO: is there a better way to give the profile to the 
        # handler?
        FakeRhizomeHandler.profile = [unhexlify(s) for s in 
                                      FAKE_RHIZOME_PROFILES[sensor_id]]
        self.sock = TCPServer((self.sensor.ip, self.sensor.port), 
                              FakeRhizomeHandler)
        info('Serving for sensor %d (%s, %s).' % (sensor_id, desc, addr))
        self.sock.serve_forever()


class Command(BaseCommand):
    args = '<sensor_id> start|stop|restart'
    help = 'Imitate the specified Rhizome device.'

    def handle(self, *args, **options):
        if len(args) == 2:
            try:
                sensor_id = int(args[0])
            except ValueError:
                raise CommandError('Invalid sensor id: \'%s\'.' % args[0])
    
            daemon = FakeRhizomeDaemon(
                settings.FAKER_PID_FILE_TEMPL % sensor_id, args=(sensor_id,), 
                stdout=(settings.FAKER_LOG_FILE_TEMPL % sensor_id),
                stderr=(settings.FAKER_LOG_FILE_TEMPL % sensor_id))
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
