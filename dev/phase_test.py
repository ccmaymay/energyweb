#!/usr/bin/python


# The systems are either single phase or three phase.  I noticed that
# the values of cwatthr in NorthDorm2 are always 0, exactly 0.
# I hypothesize that NorthDorm2, WestDorm2, and EastDorm2 are all
# single phase and that the 0 value of cwatthr is hardcoded in the
# measurement devices, or perhaps that cwatthr really looks at the
# neutral wire but there is never noticeable fluctuation from 0 W.
# (The other systems, then, are all three phase.)

# If awatthr and bwatthr are never printed, and cwatthr is printed
# only for NorthDorm2, WestDorm2, and EastDorm2, my hypothesis
# is confirmed.


import psycopg2, sys
from energyconfig import *


def main():
    conn = psycopg2.connect(PSQL_CONNSTR)
    cur = conn.cursor()

    for (k, v) in SENSORS.items():
        for d in v:
            q = ('SELECT SUM(awatthr), SUM(bwatthr), SUM(cwatthr) FROM ' 
                 + d['tb'] + ';')
            cur.execute(q)
            r = cur.fetchone()
            sys.stdout.write(d['tb'] + ':')
            if r[0] == 0:
                sys.stdout.write(' awatthr')
            if r[1] == 0:
                sys.stdout.write(' bwatthr')
            if r[2] == 0:
                sys.stdout.write(' cwatthr')
            sys.stdout.write('\n')

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
