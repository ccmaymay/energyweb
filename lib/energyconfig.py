#!/usr/bin/python


from os.path import join as _join
from logging import INFO as _INFO, DEBUG as _DEBUG


PSQL_CONNSTR = 'dbname=energy user=energy'

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = _DEBUG

MAX_SLEEP = 5

WHR_PTS_PER_AVG = 24

LOG_DIR = '/var/local/energy/log'
GRAPH_LOG_NAME = 'energygraph.log'
STATS_LOG_NAME = 'energystats.log'
MON_LOG_NAME = 'energymon.%s.log'

GRAPH_FN = 'energygraph.png'
GRAPH_DIR1 = '/tmp'
GRAPH_DIR2 = '/var/local/energy/www'
GRAPH_PATH1 = _join(GRAPH_DIR1, GRAPH_FN)
GRAPH_PATH2 = _join(GRAPH_DIR2, GRAPH_FN)

STATS_FN = 'energystats.js'
STATS_DIR1 = '/tmp'
STATS_DIR2 = '/var/local/energy/www'
STATS_PATH1 = _join(STATS_DIR1, STATS_FN)
STATS_PATH2 = _join(STATS_DIR2, STATS_FN)

SENSORS = {'Atwood': ({'tb': 'AtwoodDorm', 
                       'label': 'Atwood', 
                       'cwatthr': True, 
                       'linestyle': '-',
                       'color': '#ff0000', 
                       'ip': '172.31.10.11', 
                       'factor': 8},),
           'Case': ({'tb': 'CaseDorm', 
                     'label': 'Case', 
                     'cwatthr': True, 
                     'linestyle': '-',
                     'color': '#ff7a00', 
                     'ip': '172.31.10.31', 
                     'factor': 24},),
           'East': ({'tb': 'EastDorm1', 
                     'label': 'East 1', 
                     'cwatthr': True, 
                     'linestyle': '-',
                     'color': '#00bd39', 
                     'ip': '172.31.10.71', 
                     'factor': 4.2 / 10.0},
                    {'tb': 'EastDorm2', 
                     'label': 'East 2', 
                     'cwatthr': False, 
                     'linestyle': '-',
                     'color': '#00bd39', 
                     'ip': '172.31.10.72', 
                     'factor': 8}),
           'Linde': ({'tb': 'LindeDorm', 
                      'label': 'Linde', 
                      'cwatthr': True, 
                      'linestyle': '-',
                      'color': '#0776a0', 
                      'ip': '172.31.10.21', 
                      'factor': 16},),
           'North': ({'tb': 'NorthDorm1', 
                      'label': 'North 1', 
                      'cwatthr': True, 
                      'linestyle': '-',
                      'color': '#c10087', 
                      'ip': '172.31.10.61', 
                      'factor': 4.2 / 10.0},
                    {'tb': 'NorthDorm2', 
                     'label': 'North 2', 
                     'cwatthr': False, 
                     'linestyle': '-',
                     'color': '#40025f', 
                     'ip': '172.31.10.62', 
                     'factor': 8},
                    {'tb': 'NorthDorm3', 
                     'label': 'North HVAC', 
                     'cwatthr': True, 
                     'linestyle': '-',
                     'color': '#000000', 
                     'ip': '172.31.10.63', 
                     'factor': 4}),
           'Sontag': ({'tb': 'SontagDorm', 
                       'label': 'Sontag', 
                       'cwatthr': True, 
                       'linestyle': '-',
                       'color': '#a63f00', 
                       'ip': '172.31.10.41', 
                       'factor': 32},),
           'South': ({'tb': 'SouthDorm', 
                      'label': 'South', 
                      'cwatthr': True, 
                      'linestyle': '-',
                      'color': '#9c02a7', 
                      'ip': '172.31.10.51', 
                      'factor': 12},),
           'West': ({'tb': 'WestDorm1', 
                     'label': 'West 1', 
                     'cwatthr': True, 
                     'linestyle': '-',
                     'color': '#2e16b1', 
                     'ip': '172.31.10.81', 
                     'factor': 4.2 / 10.0},
                    {'tb': 'WestDorm2', 
                     'label': 'West 2', 
                     'cwatthr': False, 
                     'linestyle': '-',
                     'color': '#5c5c5c', 
                     'ip': '172.31.10.82', 
                     'factor': 8},
                    {'tb': 'EastDorm3', 
                     'label': 'West HVAC', 
                     'cwatthr': True, 
                     'linestyle': '-',
                     'color': '#638700', 
                     'ip': '172.31.10.73', 
                     'factor': 6})}
