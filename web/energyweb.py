#!/usr/bin/env python


'''
web.py application to power the (presently very small) web interface
'''


import sys
sys.path.append('/var/local/energy/lib')
import web, psycopg2, simplejson, datetime, calendar
from energyconfig import *


web.config.debug = WEB_DEBUG


render = web.template.render(WEB_TEMPLATES)

urls = (
    '/', 'index',
    '/data(\d*).json', 'index_data',
)

app = web.application(urls, globals())

class index(object):
    '''
    This is the main view.  A javascript-generated graph of current
    power usage is displayed above a table of running averages.  This
    view provides the HTML; the other view provides the data.
    '''

    def GET(self):
        conn = psycopg2.connect(PSQL_CONNSTR)
        cur = conn.cursor()

        # Create an array of arrays to efficiently store information
        # for automatically generating the table of averages.  Sensors will
        # be grouped by sensor groups, and both levels (sensor groups and
        # the sensors within them) will be ordered by increasing id for
        # consistency.  This all makes the templating engine's job easier.
        cur.execute('''SELECT sensors.id, sensors.name, 
                         sensors.sensor_group_id, sensor_groups.name
                       FROM sensors
                       INNER JOIN sensor_groups 
                         ON sensor_groups.id = sensors.sensor_group_id
                       ORDER BY sensor_groups.id ASC, sensors.id ASC;''')
        sensor_structure = []
        for r in cur:
            if len(sensor_structure) > 0 and sensor_structure[-1][0] == r[2]:
                sensor_structure[-1][2].append((r[0], r[1]))
            else:
                sensor_structure.append((r[2], r[3], [(r[0], r[1]),]))

        return render.index(sensor_structure)


class index_data(object):
    '''
    This view provides the data that powers the index view.  This is
    not a trivial task.  A balance is hopefully achieved between server-
    and client-side processing, but things may need to be adjusted in
    the future.
    '''

    def GET(self, data=None):
        '''
        Return JSON data for generating a graph and table of usage
        averages.  If data is supplied, it is expected to represent
        a timestamp; return only those graph points since (and
        including) that timestamp.
        '''

        conn = psycopg2.connect(PSQL_CONNSTR)
        cur = conn.cursor()

        # We first set up a couple of arrays for getting at sensor
        # and sensor group information, like the index view.  This is
        # probably not optimal; it works for the time being.
        cur.execute('''SELECT id, name, sensor_group_id
                       FROM sensors ORDER BY id ASC;''')
        sensors = {}
        sg_sensors = {}
        for r in cur:
            sensors[r[0]] = r[1:]
            if sg_sensors.has_key(r[2]):
                sg_sensors[r[2]].append(r[0])
            else:
                sg_sensors[r[2]] = [r[0]]
        num_sensors = len(sensors)

        cur.execute('''SELECT id, name, color
                       FROM sensor_groups ORDER BY id ASC;''')
        sensor_groups = {}
        sensor_structure = []
        for r in cur:
            sensor_groups[r[0]] = r[1:]
            sensor_structure.append((r[0], sg_sensors[r[0]]))

        # We will display only the latest averages for the user, so
        # assume the latest average is calculated for each sensor 
        # (within a given average type).  If some averages have not
        # been computed---so our query returns several of the latest
        # time-period averages, but also some averages from the past,
        # and hence does not contain the latest averages for all
        # sensors---then return None in their place.

        cur.execute('''SELECT sensor_id, date_trunc('week', rdngtime_first), 
                         watts / 1000
                       FROM power_averages
                       WHERE avg_type = %s
                       ORDER BY date_trunc('week', rdngtime_first) DESC
                       LIMIT %s;''',
                    (AVG_TYPE_WEEK, num_sensors))
        week_averages = {}
        first_row = True
        for r in cur:
            if first_row:
                week_rdngtime_trunc = r[1]
                first_row = False
            if r[1] == week_rdngtime_trunc:
                week_averages[r[0]] = r[2]

        # (Do the same for monthly averages)

        cur.execute('''SELECT sensor_id, date_trunc('month', rdngtime_first), 
                         watts / 1000
                       FROM power_averages
                       WHERE avg_type = %s
                       ORDER BY date_trunc('month', rdngtime_first) DESC
                       LIMIT %s;''',
                    (AVG_TYPE_MONTH, num_sensors))
        month_averages = {}
        first_row = True
        for r in cur:
            if first_row:
                month_rdngtime_trunc = r[1]
                first_row = False
            if r[1] == month_rdngtime_trunc:
                month_averages[r[0]] = r[2]

        # Now, calculate the data points for the graph we're going to
        # display.  This is harder than it should be since the points
        # are pulled from a practically continuous range of times,
        # but we want to somehow sum the lines within a given sensor
        # group---we want West Dorm's power usage, not the usages on
        # West's three individual sensors.  Stochastic simulation may
        # have something very interesting to say about this, but for
        # the time being we will settle for summing points within
        # ten-second intervals.  The javascript can then deal with
        # the null values (the infrequent cases when no reading appears
        # within one of these 10-second bins for a certain sensor) as
        # it desires.  3 hours, by the way, is the length of time to
        # be represented on the graph.

        # If the client has supplied data (a string of digits in the
        # URL---representing seconds since the epoch), then we only
        # consider data since (and including) that timestamp.
        exe_args = ['''SELECT AVG(watts) / 1000, sid, rdngtime_per
                       FROM 
                         (SELECT sensor_readings.awatthr 
                         + sensor_readings.bwatthr 
                         + sensor_readings.cwatthr AS watts, sensors.id AS sid, 
                         sensors.sensor_group_id AS sgid,
                         date_trunc('minute', sensor_readings.rdngtime)
                         + FLOOR(EXTRACT(SECOND FROM sensor_readings.rdngtime)
                         / 10) * interval '10 seconds' AS rdngtime_per
                         FROM sensor_readings
                         INNER JOIN sensors 
                           ON sensor_readings.sensor_id = sensors.id
                         WHERE now() - rdngtime <= interval '3 hours')
                         AS rdngtime_per_subq '''
                    + (data and 'WHERE %s <= rdngtime_per' or '') + '''
                       GROUP BY rdngtime_per, sid
                       ORDER BY rdngtime_per ASC, sid ASC;''']

        if data:
            last_per = datetime.datetime.utcfromtimestamp(int(data) / 1000)
            exe_args.append((last_per,))

        cur.execute(*exe_args)

        # Also note, above, that if data was supplied then we selected
        # everything since the provided timestamp's truncated date,
        # including that date.  We will always provide the client with
        # a new copy of the latest record he received last time, since
        # that last record may have changed (more sensors may have
        # submitted measurements and added to it).  The second to
        # latest and older records, however, will never change.

        # Now organize the query in a format amenable to the (javascript)
        # client.  (We essentially transpose the array of information
        # returned so that the client will have an array of the sensor
        # reading times and an array for sensor containing the power
        # readings at those times.)
        y = {}
        iter_num = 1
        r = cur.fetchone()
        per = r[2]
        while r is not None:
            x = int(calendar.timegm(per.timetuple()) * 1000)
            for sensor_id in sensors.keys():
                sg_id = sensors[sensor_id][1]
                if not y.has_key(sg_id):
                    y[sg_id] = []
                if r[2] == per and r[1] == sensor_id:
                    if len(y[sg_id]) < iter_num:
                        y[sg_id].append([x, float(r[0])])
                    else:
                        if y[sg_id][-1][1] is not None:
                            y[sg_id][-1][1] += float(r[0])
                    r = cur.fetchone()
                    if r is None:
                        last_record = x
                        break
                else:
                    if len(y[sg_id]) < iter_num:
                        y[sg_id].append([x, None])
                    else:
                        y[sg_id][-1][1] = None
            per += datetime.timedelta(0, 10, 0)
            iter_num += 1

        # Once more, if the client has indicated that they have
        # data up to a certain point, we save bandwidth and client
        # processing time by only sending the new information.
        web.header('Content-Type', 'application/json')
        if data:
            return simplejson.dumps({'y': y,
                                     'last_record': last_record, 
                                     'week_averages': week_averages, 
                                     'month_averages': month_averages})
        else:
            return simplejson.dumps({'y': y,
                                     'sensors': sensors,
                                     'sensor_groups': sensor_groups,
                                     'sensor_structure': sensor_structure,
                                     'last_record': last_record, 
                                     'week_averages': week_averages, 
                                     'month_averages': month_averages})


if __name__ == '__main__':
    app.run()
