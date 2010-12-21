#!/usr/bin/env python


'''
Create the database structure for the monitoring program and the scripts
that operate on the data.  Populate it with some random rows for development
purposes.

This file essentially contains the current (as of writing) configuration
of sensors (and groups) on campus.
'''

import sys
sys.path.append('/var/local/energy/lib')
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from random import random, randint
from energyconfig import *


def main():
    '''
    Build the database structure and populate with random rows.
    '''
    conn = psycopg2.connect(PSQL_CONNSTR)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE sensor_groups 
                     (id serial primary key, 
                     name varchar(32) not null unique, 
                     color char(6));''')
    cur.execute('''CREATE TABLE sensors 
                     (id serial primary key, 
                     name varchar(32) not null,
                     ip inet, 
                     port integer, 
                     sensor_group_id integer REFERENCES sensor_groups (id), 
                     three_phase boolean, 
                     factor double precision,
                     UNIQUE(name, sensor_group_id));''')

    # (The colors are for graphing purposes.)
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('Atwood', '00bd39');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('Case', '0776a0');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('East', '6600cc');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('Linde', 'd100a0');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('North', 'ff0000');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('Sontag', 'ffa000');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('South', 'a63f00');''')
    cur.execute('''INSERT INTO sensor_groups (name, color) 
                   VALUES ('West', '000000');''')

    # Determine IDs of sensor groups for later use
    cur.execute('''SELECT id, name FROM sensor_groups;''')
    sensor_groups = {}
    for r in cur:
        sensor_groups[r[1]] = r[0]

    # Insert sensor information---the important part.
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('', '172.31.10.11', %s, 
                     'true', 8, 4001);''', 
                (sensor_groups['Atwood'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('', '172.31.10.31', %s, 
                     'true', 24, 4001);''', 
                (sensor_groups['Case'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('1', '172.31.10.71', %s, 
                     'true', 4.2, 4001);''', 
                (sensor_groups['East'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('2', '172.31.10.72', %s, 
                     'false', 8, 4001);''', 
                (sensor_groups['East'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('', '172.31.10.21', %s, 
                     'true', 16, 4001);''', 
                (sensor_groups['Linde'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('1', '172.31.10.61', %s, 
                     'true', 4.2 / 10.0, 4001);''', 
                (sensor_groups['North'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('2', '172.31.10.62', %s, 
                     'false', 8, 4001);''', 
                (sensor_groups['North'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('HVAC', '172.31.10.63', %s, 
                     'true', 4, 4001);''', 
                (sensor_groups['North'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('', '172.31.10.41', %s, 
                     'true', 32, 4001);''', 
                (sensor_groups['Sontag'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('', '172.31.10.51', %s, 
                     'true', 12, 4001);''', 
                (sensor_groups['South'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('1', '172.31.10.81', %s, 
                     'true', 4.2 / 10.0, 4001);''', 
                (sensor_groups['West'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('2', '172.31.10.82', %s, 
                     'false', 8, 4001);''', 
                (sensor_groups['West'],))
    cur.execute('''INSERT INTO sensors (name, ip, sensor_group_id, 
                     three_phase, factor, port) 
                   VALUES ('HVAC', '172.31.10.73', %s, 
                     'true', 6, 4001);''', 
                (sensor_groups['West'],))

    # For a note about three phase sensors, see the monitoring program
    cur.execute('''SELECT id, name, three_phase FROM sensors;''')
    sensors = {}
    phase_factor = {}
    for r in cur:
        sensors[r[0]] = r[1]
        phase_factor[r[0]] = (r[2] and 1 or 0)

    # This is the central table where data is stored directly from the sensors
    cur.execute('''CREATE TABLE sensor_readings
                     (rdngtime timestamp not null, 
                     sensor_id integer REFERENCES sensors (id),
                     rindex smallint,
                     awatthr integer, 
                     bwatthr integer, 
                     cwatthr integer, 
                     avarhr integer, 
                     bvarhr integer, 
                     cvarhr integer, 
                     avahr integer, 
                     bvahr integer, 
                     cvahr integer, 
                     airms integer, 
                     birms integer, 
                     cirms integer, 
                     avrms integer, 
                     bvrms integer, 
                     cvrms integer, 
                     freq integer, 
                     tempc integer);''')
    cur.execute('''CREATE INDEX sensor_readings_index 
                   ON sensor_readings (rdngtime);''')

    # This table will be for averages (per week, and per month) of power
    # readings.  Postgres doesn't seem to like to compute these for each
    # web request, whereas the 10 seconds in between messages from a
    # sensor offer plenty of thinking time.
    cur.execute('''CREATE TABLE power_averages 
                     (rdngtime_trunc timestamp not null,
                     rdngtime_first timestamp not null,
                     rdngtime_last timestamp not null,
                     sensor_id integer REFERENCES sensors (id),
                     avg_type character varying(16) not null,
                     num_pts integer,
                     watts double precision,
                     UNIQUE(sensor_id, avg_type, rdngtime_trunc));''')

    cur.execute('''CREATE INDEX power_averages_rdngtime_trunc_index 
                   ON power_averages (rdngtime_trunc);''')
    cur.execute('''CREATE INDEX power_averages_avg_type_index 
                   ON power_averages (avg_type);''')

    cur.execute('''CREATE INDEX sensor_readings_rdngtime_per_index 
                   ON sensor_readings ((date_trunc('minute'::text, rdngtime)
                     + (FLOOR((date_part('second'::text, rdngtime) 
                     / 10::double precision)) * '00:00:10'::interval)));''')

    cur.execute('''CREATE INDEX sensor_readings_rdngtime_mper_index 
                   ON sensor_readings (date_trunc('minute'::text, 
                     rdngtime));''')

    # A view for convenience
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


if __name__ == '__main__':
    main()
