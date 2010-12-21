#!/usr/bin/env python


'''
Application configuration parameters go here.
'''


from os.path import join as _join
from logging import INFO as _INFO, DEBUG as _DEBUG


# AVG_TYPES is a tuple of time periods over which readings will be
# averaged (the averages being stored in power_averages).  The values
# are strings, expected to correspond to the inputs to the PostgreSQL
# function date_trunc.  See:
# http://www.postgresql.org/docs/8.4/interactive/functions-datetime.html
AVG_TYPES = ('month', 'week', 'day', 'hour', 'minute')

MON_USAGE_TEMPL = 'usage: %s <sensor_id> start|stop|restart'

MON_PID_FILE_TEMPL = '/var/local/energy/run/energymon.%d.pid'
MON_LOG_FILE_TEMPL = '/var/local/energy/log/energymon.%d.log'

FAKER_USAGE_TEMPL = 'usage: %s <sensor_id> start|stop|restart'

FAKER_PID_FILE_TEMPL = '/var/local/energy/run/energyfaker.%d.pid'
FAKER_LOG_FILE_TEMPL = '/var/local/energy/log/energyfaker.%d.log'

FAKER_SLEEP_VARIATION = 0.1

PSQL_CONNSTR = 'dbname=energy user=energy'

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = _INFO

WEB_DEBUG = False

WEB_TEMPLATES = '/var/local/energy/web/templates/'

# If a socket error is encountered, wait this many seconds before
# trying to reconnect.
ERROR_PAUSE = 9
