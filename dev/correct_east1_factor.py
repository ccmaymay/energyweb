#!/usr/bin/env python


'''
The multiplier for East 1 was discovered to be too low (by a factor of
10).  Correct that by updating the sensor parameters, updating all
stored readings, then recreating the averages in power_averages.

Ensure the East 1 monitoring script is stopped before running this!
Otherwise things may get *very* messy.
'''


import sys
sys.path.append('/var/local/energy/lib')
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from energyconfig import *


EAST1_SENSOR_ID = 3
EAST1_FACTOR_FACTOR = 10 # multiply the current factor by 10


def main():
    conn = psycopg2.connect(PSQL_CONNSTR)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Update the factor
    cur.execute('''UPDATE sensors SET factor = factor * %s WHERE id = %s;''',
                (EAST1_FACTOR_FACTOR, EAST1_SENSOR_ID))

    # Update sensor_readings
    cur.execute('''UPDATE sensor_readings 
                   SET (awatthr, bwatthr, cwatthr, 
                     avarhr, bvarhr, cvarhr,
                     avahr, bvahr, cvahr, 
                     airms, birms, cirms) =
                     (awatthr * %s, bwatthr * %s, cwatthr * %s, 
                     avarhr * %s, bvarhr * %s, cvarhr * %s,
                     avahr * %s, bvahr * %s, cvahr * %s, 
                     airms * %s, birms * %s, cirms * %s)
                   WHERE
                     sensor_id = %s;''',
                (EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR,
                 EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR,
                 EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR,
                 EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR, EAST1_FACTOR_FACTOR,
                 EAST1_SENSOR_ID))

    # "Update" power_averages by deleting and recreating
    cur.execute('''DELETE FROM power_averages WHERE sensor_id = %s;''',
                (EAST1_SENSOR_ID,))
    cur.execute('''INSERT INTO power_averages (rdngtime_first, 
                     rdngtime_last, sensor_id, avg_type, num_pts, watts) 
                   SELECT MIN(rdngtime), MAX(rdngtime), %s, %s, COUNT(*), 
                     AVG(awatthr + bwatthr + cwatthr) 
                     FROM sensor_readings
                     WHERE sensor_id = %s
                     GROUP BY date_trunc('month', rdngtime);''',
                (EAST1_SENSOR_ID, AVG_TYPE_MONTH, EAST1_SENSOR_ID))
    cur.execute('''INSERT INTO power_averages (rdngtime_first, 
                     rdngtime_last, sensor_id, avg_type, num_pts, watts) 
                   SELECT MIN(rdngtime), MAX(rdngtime), %s, %s, COUNT(*), 
                     AVG(awatthr + bwatthr + cwatthr) 
                     FROM sensor_readings
                     WHERE sensor_id = %s
                     GROUP BY date_trunc('week', rdngtime);''',
                (EAST1_SENSOR_ID, AVG_TYPE_WEEK, EAST1_SENSOR_ID))


if __name__ == '__main__':
    main()
