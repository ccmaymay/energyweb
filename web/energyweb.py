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
    '/data(\d*)(-.+)?.json', 'index_data',
)

app = web.application(urls, globals())

def get_sensor_groups(cur):
    '''
    Return a list of sensor groups, each of which is represented as a
    list of values: [id, name, color, sensors] .
    sensors is a list of sensors, each of which is represented as a 
    list of values: [id, name] . 
    '''

    cur.execute('''SELECT sensor_groups.id, sensor_groups.name, 
                     sensor_groups.color, sensors.id, sensors.name
                   FROM sensors
                   INNER JOIN sensor_groups 
                     ON sensors.sensor_group_id = sensor_groups.id
                   ORDER BY sensor_groups.id ASC, sensors.id ASC;''')

    sensor_groups = []
    for r in cur:
        if len(sensor_groups) > 0 and sensor_groups[-1][0] == r[0]:
            # We have already created an element in sensor_groups for
            # this group, so just add this sensor's data to it.
            sensor_groups[-1][3].append(r[3:])
        else:
            # Create a new element in sensor_groups, including this
            # sensor's data.
            sensor_groups.append([r[0], r[1], r[2], [r[3:]]])

    return sensor_groups

class index(object):
    '''
    This is the main view.  A javascript-generated graph of current
    power usage is displayed above a table of running averages.  This
    view provides the HTML; the other view provides the data.
    '''

    def GET(self):
        conn = psycopg2.connect(PSQL_CONNSTR)
        cur = conn.cursor()

        return render.index(get_sensor_groups(cur))


class index_data(object):
    '''
    This view provides the data that powers the index view.  This is
    not a trivial task.  A balance is hopefully achieved between server-
    and client-side processing, but things may need to be adjusted in
    the future.
    '''

    def GET(self, data=None, junk=None):
        '''
        Return JSON data for generating a graph and table of usage
        averages.  If data is supplied, it is expected to represent
        a UTC timestamp; return only those graph points since (and
        including) that timestamp.

        The presence of junk is merely to allow arbitrary/spontaneous
        URLs (for purpose of preventing caching in certain browsers).
        '''

        conn = psycopg2.connect(PSQL_CONNSTR)
        cur = conn.cursor()

        sensor_groups = get_sensor_groups(cur)
        num_sensors = 0
        for sg in sensor_groups:
            num_sensors += len(sg[3])

        # We will display only the latest averages for the user, so
        # assume the latest average is calculated for each sensor 
        # (within a given average type).  If some averages have not
        # been computed---so our query returns several of the latest
        # time-period averages, but also some averages from the past,
        # and hence does not contain the latest averages for all
        # sensors---then return None in their place.

        cur.execute('''SELECT sensor_id, date_trunc('week', 
                         rdngtime_first), watts / 1000
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

        cur.execute('''SELECT sensor_id, date_trunc('month', 
                         rdngtime_first), watts / 1000
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
        # West's three individual sensors.  Stochastic simulation (e.g.)
        # may have something very interesting to say about this, but for
        # the time being we will settle for summing points within
        # ten-second intervals.  The client (javascript) can then deal
        # with the null values (the infrequent cases when no reading
        # appears within one of these 10-second bins for a certain
        # sensor) as it desires.  (3 hours, by the way, is the length of
        # time to be represented on the graph.)

        # rdngtime_per in the query below is a timestamp representing
        # the ten-second interval to which the current reading belongs.

        # If the client has supplied data (a string of digits in the
        # URL---representing UTC seconds since the epoch), then we only
        # consider data since (and including) that timestamp.
        exe_args = ['''SELECT AVG(watts) / 1000, sid, rdngtime_per
                       FROM 
                         (SELECT sensor_readings.awatthr 
                           + sensor_readings.bwatthr 
                           + sensor_readings.cwatthr AS watts, 
                           sensors.id AS sid, 
                           sensors.sensor_group_id AS sgid,
                           date_trunc('minute', 
                           sensor_readings.rdngtime)
                           + FLOOR(EXTRACT(SECOND FROM 
                           sensor_readings.rdngtime) / 10) 
                           * interval '10 seconds' AS rdngtime_per
                         FROM sensor_readings
                         INNER JOIN sensors 
                           ON sensor_readings.sensor_id = sensors.id
                         WHERE now() - rdngtime <= interval '3 hours')
                         AS rdngtime_per_subq '''
                    # If data was supplied, only take a subset of the 
                    # rows
                    + (data and 'WHERE %s <= rdngtime_per' or '') + '''
                       GROUP BY rdngtime_per, sgid, sid
                       ORDER BY rdngtime_per ASC, sgid ASC, sid ASC;''']

        if data:
            # Remember the timestamp represents UTC.  JavaScript
            # represents times in ms since epoch, hence the division.
            last_per = datetime.datetime.utcfromtimestamp(int(data) 
                / 1000)
            exe_args.append((last_per,))

        cur.execute(*exe_args)

        # Also note, above, that if data was supplied then we selected
        # everything since the provided timestamp's truncated date,
        # including that date.  We will always provide the client with
        # a new copy of the latest record he received last time, since
        # that last record may have changed (more sensors may have
        # submitted measurements and added to it).  The second to
        # latest and older records, however, will never change.

        # Now organize the query in a format amenable to the 
        # (javascript) client.  (The grapher wants (x, y) pairs.)

        sg_xy_pairs = dict([[sg[0], []] for sg in sensor_groups])
        r = cur.fetchone()
        per = r[2]

        # At the end of each outer loop, we increment per (the current
        # ten-second period of time we're considering) by ten seconds.
        while r is not None:
            # Remember that the JavaScript client takes (and
            # gives) UTC timestamps in ms
            x = int(calendar.timegm(per.timetuple()) * 1000)
            for sg in sensor_groups:
                y = 0
                for s in sg[3]:
                    # If this sensor has a reading for the current per,
                    # update y.  There are three ways the sensor might
                    # not have such a reading:
                    # 1. r is None, i.e. there are no more readings at
                    #    all
                    # 2. r is not None and r[2] > per, i.e. there are 
                    #    more readings but not for this per
                    # 3. r is not None and r[2] <= per and r[1] != s[0],
                    #    i.e. there are more readings for this per,
                    #    but none for this sensor
                    if r is not None and r[2] <= per and r[1] == s[0]:
                        # If y is None, leave it as such.   Else, add
                        # this sensor reading to y.  Afterwards, in
                        # either case, fetch a new row.
                        if y is not None:
                            y += float(r[0])
                        r = cur.fetchone()
                    else:
                        y = None
                sg_xy_pairs[sg[0]].append((x, y))
            per += datetime.timedelta(0, 10, 0)

        last_record = x

        # If the client has indicated that they have
        # data up to a certain point, we save bandwidth and client
        # processing time by only sending the new information.
        web.header('Content-Type', 'application/json')
        if data:
            return simplejson.dumps({'sg_xy_pairs': sg_xy_pairs,
                                     'last_record': last_record, 
                                     'week_averages': week_averages, 
                                     'month_averages': month_averages})
        else:
            return simplejson.dumps({'sg_xy_pairs': sg_xy_pairs,
                                     'sensor_groups': sensor_groups,
                                     'last_record': last_record, 
                                     'week_averages': week_averages, 
                                     'month_averages': month_averages})


if __name__ == '__main__':
    app.run()
