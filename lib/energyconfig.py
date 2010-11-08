#!/usr/bin/env python


'''
Application configuration parameters go here.
'''


from os.path import join as _join
from logging import INFO as _INFO


# AVG_TYPE_* are constants for easy identification of average types 
# e.g. in the SQL database.  Right now there are only two.
AVG_TYPE_WEEK = 1
AVG_TYPE_MONTH = 2

MON_USAGE_TEMPL = 'usage: %s <sensor_id> start|stop|restart'

MON_PID_FILE_TEMPL = '/var/local/energy/run/energymon.%d.pid'
MON_LOG_FILE_TEMPL = '/var/local/energy/log/energymon.%d.log'

PSQL_CONNSTR = 'dbname=energy user=energy'

# All sensors have been configured to use the same port.
SENSOR_TCP_PORT = 4001

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = _INFO

WEB_DEBUG = False

WEB_TEMPLATES = '/var/local/energy/web/templates/'

# If a socket error is encountered, wait this many seconds before
# trying to reconnect.
ERROR_PAUSE = 9
