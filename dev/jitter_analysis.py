#!/usr/bin/env python


import psycopg2, matplotlib, sys, os.path
sys.path.append('/var/local/energy/lib')
from energyconfig import *
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


SECS_FMT = mdates.DateFormatter('%l:%M:%S')
YCOLS = ('awatthr', 'bwatthr', 'cwatthr', 'avarhr', 'bvarhr', 'cvarhr', 
         'avahr', 'bvahr', 'cvahr', 'airms', 'birms', 'cirms', 'avrms', 
         'bvrms', 'cvrms', 'freq', 'tempc')
FN = os.path.join(sys.argv[1], '%s.png')


def main():
    conn = psycopg2.connect(PSQL_CONNSTR)
    cur = conn.cursor()

    for (k, v) in SENSORS.items():
        for d in v:
            q = ('SELECT rdngtime, ' + ', '.join(YCOLS) + ' FROM ' 
                 + d['tb'] + ' WHERE '
                 + 'rdngtime >= timestamp \'2010-11-03 19:46\' '
                 + 'AND rdngtime <= timestamp \'2010-11-03 19:48\' '
                 + 'ORDER BY rdngtime ASC;')
            cur.execute(q)
            x = []
            y = [[] for c in YCOLS]
            for record in cur:
                x.append(record[0])
                for i in range(len(YCOLS)):
                    y[i].append(record[i+1])
            fig = plt.figure(figsize=(16,16))
            ax = fig.add_subplot(111)
            for i in range(len(YCOLS)):
                z = float(i+1)/len(YCOLS)
                plt.plot_date(x, y[i], '-', label=YCOLS[i],
                              marker='o',
                              color=((z, 0, 1-z)), xdate=True, 
                              ydate=False, linewidth=1.5)
            #ax.xaxis.set_major_locator(SECS_LOC)
            ax.xaxis.set_major_formatter(SECS_FMT)
            (ymin, ymax) = plt.ylim()
            ymax *= 6.0/5.0 # Seems to work
            plt.ylim(ymin, ymax)
            plt.legend(loc='upper left', ncol=7)
            plt.xlabel('time')
            ax.grid(True)
            #fig.autofmt_xdate() # rotate x-axis labels nicely
            plt.savefig(FN % d['tb'], bbox_inches='tight')
            plt.clf()
            plt.close('all')

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
