#!/usr/bin/env python


'''
Insert missing power averages for all sensors, based on sensor 
readings already in the database.
'''


from django.core.management.base import BaseCommand, CommandError
from energyweb.graph.models import Sensor, PowerAverage, SensorReading
from django.db import connection, transaction


class Command(BaseCommand):
    args = ''
    help = 'Insert missing power averages for all sensors.'

    def handle(self, *args, **options):
        for sensor in Sensor.objects.all():
            cur = connection.cursor()
            power_average_qs = PowerAverage.objects.filter(
                sensor=sensor).order_by('-trunc_reading_time')
            sensor_reading_qs = SensorReading.objects.filter(
                sensor=sensor).order_by('-reading_time')

            try:
                latest_reading = sensor_reading_qs.latest('reading_time')
            except SensorReading.DoesNotExist:
                pass # No readings: nothing to do.
            else:
                print 'Inserting missing averages for sensor %d:' % sensor.id
                for average_type in PowerAverage.AVERAGE_TYPES:
                    # Don't confuse trunc_latest_reading_time with the
                    # similarly-named column of graph_poweraverage.
                    # trunc_latest_reading_time is the truncated
                    # reading_time of the latest row in graph_sensorreading
                    # for this sensor.
                    trunc_latest_reading_time = PowerAverage.date_trunc(
                        average_type, latest_reading.reading_time)

                    r = PowerAverage.insert_averages(cur, average_type, sensor,
                        trunc_latest_reading_time)
                    transaction.commit_unless_managed()
                    print '    \'%s\': %d rows' % (average_type, r)
