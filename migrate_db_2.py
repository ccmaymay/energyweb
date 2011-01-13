#!/usr/bin/env python


'''
Migrate the database.

NOTE:  This cannot be applied directly after the original migration.
It is intended only to automate the migration for a certain range of
commits to the source code.

In order to perform a full migration from the original Rhizome setup, 
it would be best to start from scratch, using dev/create_db.py as a
guide.
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

    # Add port column to sensors
    cur.execute('''ALTER TABLE sensors 
                   ADD COLUMN port integer;''')
    cur.execute('''UPDATE sensors 
                   SET port = 4001;''')

    # Update convenience view to show port
    cur.execute('''DROP VIEW sensors_with_groups;''')
    cur.execute('''CREATE VIEW sensors_with_groups 
                   AS SELECT sensor_groups.id AS sensor_group_id, 
                     sensors.id AS sensor_id, 
                     sensor_groups.name AS sensor_group_name, 
                     sensors.name AS sensor_name, 
                     sensor_groups.color AS sensor_group_color, 
                     sensors.ip AS sensor_ip, 
                     sensors.port AS sensor_port, 
                     sensors.factor AS sensor_factor, 
                     sensors.three_phase AS sensor_three_phase
                   FROM sensors
                   LEFT JOIN sensor_groups 
                     ON sensors.sensor_group_id = sensor_groups.id
                   ORDER BY sensor_groups.id, sensors.id;''')

    # Change avg_type column to be a string in power_averages
    cur.execute('''ALTER TABLE power_averages 
                   RENAME COLUMN avg_type TO avg_type_num;''')
    cur.execute('''ALTER TABLE power_averages 
                   ADD COLUMN avg_type character varying(16);''')
    cur.execute('''UPDATE power_averages
                   SET avg_type = 'week'
                   WHERE avg_type_num = 1;''')
    cur.execute('''UPDATE power_averages
                   SET avg_type = 'month'
                   WHERE avg_type_num = 2;''')
    cur.execute('''ALTER TABLE power_averages 
                   ALTER COLUMN avg_type SET not null;''')
    cur.execute('''ALTER TABLE power_averages
                   DROP COLUMN avg_type_num;''')

    # Add rdngtime_trunc column to power_averages
    cur.execute('''ALTER TABLE power_averages 
                   ADD COLUMN rdngtime_trunc timestamp;''')
    cur.execute('''UPDATE power_averages
                   SET rdngtime_trunc =
                     date_trunc(avg_type, rdngtime_first);''')
    cur.execute('''ALTER TABLE power_averages 
                   ALTER COLUMN rdngtime_trunc SET not null;''')

    # Redefine unique constraint on power_averages wrt rdngtime_trunc
    # (original constraint was removed when avg_type was renamed and
    # dropped).
    cur.execute('''ALTER TABLE power_averages
                   ADD
                     UNIQUE(sensor_id, avg_type, rdngtime_trunc);''')

    # Remove indexes on rdngtime_first and rdngtime_last in 
    # power_averages, and replace with an index on rdngtime_trunc
    cur.execute('''DROP INDEX power_averages_first_index;''')
    cur.execute('''DROP INDEX power_averages_last_index;''')
    cur.execute('''CREATE INDEX power_averages_rdngtime_trunc_index 
                   ON power_averages (rdngtime_trunc);''')

    # Populate power_averages using existing data
    for avg_type in AVG_TYPES:
        if avg_type in ('week', 'month'):
            continue
        cur.execute('''INSERT INTO power_averages
                         (rdngtime_first, rdngtime_last, rdngtime_trunc,
                         sensor_id, avg_type, num_pts, watts)
                       SELECT MIN(rdngtime), MAX(rdngtime), 
                           date_trunc(%s, rdngtime) as rdngtime_trunc_selected,
                           sensor_id, %s, COUNT(*), 
                           AVG(awatthr + bwatthr + cwatthr)
                         FROM sensor_readings
                         GROUP BY rdngtime_trunc_selected, sensor_id;''',
                    (avg_type, avg_type))


if __name__ == '__main__':
    main()
