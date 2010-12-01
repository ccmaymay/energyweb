#!/usr/bin/env python


'''
Migrate the database from the original setup (one table per dorm) to 
the new one (sensor_readings, power_averages contain all data).
'''


import sys
sys.path.append('/var/local/energy/lib')
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from energyconfig import *


def main():
    conn = psycopg2.connect(PSQL_CONNSTR)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    sensors = ['AtwoodDorm', 'CaseDorm', 'EastDorm1', 'EastDorm2', 'LindeDorm', 
               'NorthDorm1', 'NorthDorm2', 'NorthDorm3', 'SontagDorm', 
               'SouthDorm', 'WestDorm1', 'WestDorm2', 'EastDorm3']
    # sensor ids of single phase sensors
    sp = [4, 7, 12]

    for sensor_id in range(len(sensors)):
        # pf = phase factor.  1 if three phase, 0 if single phase
        pf = 1 - (((sensor_id + 1) in sp) and 1 or 0)
        cur.execute('''INSERT INTO sensor_readings (rdngtime, sensor_id,
                         rindex, awatthr, bwatthr, cwatthr, avarhr, bvarhr, 
                         cvarhr, avahr, bvahr, cvahr, airms, birms, cirms, 
                         avrms, bvrms, cvrms, freq, tempc) 
                       SELECT rdngtime, %s, 0,
                         FLOOR(awatthr), FLOOR(bwatthr), FLOOR(%d * cwatthr),
                         FLOOR(avarhr), FLOOR(bvarhr), FLOOR(cvarhr),
                         FLOOR(avahr), FLOOR(bvahr), FLOOR(cvahr),
                         FLOOR(airms), FLOOR(birms), FLOOR(cirms),
                         FLOOR(avrms), FLOOR(bvrms), FLOOR(cvrms),
                         FLOOR(freq), FLOOR(tempc)
                       FROM %s;'''
                    % (sensor_id + 1, pf, sensors[sensor_id]))
        cur.execute('''INSERT INTO power_averages (rdngtime_first, 
                         rdngtime_last, sensor_id, avg_type, num_pts, watts) 
                       SELECT MIN(rdngtime), MAX(rdngtime), %s, %s, COUNT(*), 
                         AVG(awatthr + bwatthr + cwatthr) 
                         FROM sensor_readings
                         WHERE sensor_id = %s
                         GROUP BY date_trunc('month', rdngtime);''',
                    (sensor_id + 1, AVG_TYPE_MONTH, sensor_id + 1))
        cur.execute('''INSERT INTO power_averages (rdngtime_first, 
                         rdngtime_last, sensor_id, avg_type, num_pts, watts) 
                       SELECT MIN(rdngtime), MAX(rdngtime), %s, %s, COUNT(*), 
                         AVG(awatthr + bwatthr + cwatthr) 
                         FROM sensor_readings
                         WHERE sensor_id = %s
                         GROUP BY date_trunc('week', rdngtime);''',
                    (sensor_id + 1, AVG_TYPE_WEEK, sensor_id + 1))


if __name__ == '__main__':
    main()
