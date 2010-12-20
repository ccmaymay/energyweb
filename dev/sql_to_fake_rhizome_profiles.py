#!/usr/bin/env python


import sys
sys.path.append('/var/local/energy/lib')
import psycopg2, datetime
from binascii import hexlify
from energyconfig import *


RDNGTIME_START = datetime.datetime(2010, 11, 1, 0, 0, 0)
RDNGTIME_END = datetime.datetime(2010, 11, 2, 0, 0, 0)


def main():
    conn = psycopg2.connect(PSQL_CONNSTR)
    cur = conn.cursor()

    cur.execute('''SELECT id, factor FROM sensors;''')
    sensor_data = []
    for r in cur:
        sensor_data.append(list(r))

    print '#!/usr/bin/env python'
    print '\n'
    print 'TESTING_SOCKET_PROFILES = {'
    for (s_id, factor) in sensor_data:
        print '    %d: (' % s_id
        cur.execute('''SELECT rdngtime, rindex, 
                         CAST (awatthr / %s AS integer),
                         CAST (bwatthr / %s AS integer),
                         CAST (cwatthr / %s AS integer),
                         CAST (avarhr / %s AS integer),
                         CAST (bvarhr / %s AS integer),
                         CAST (cvarhr / %s AS integer),
                         CAST (avahr / %s AS integer),
                         CAST (bvahr / %s AS integer),
                         CAST (cvahr / %s AS integer),
                         CAST (airms / %s AS integer),
                         CAST (birms / %s AS integer),
                         CAST (cirms / %s AS integer),
                         avrms, bvrms, cvrms, 
                         freq, (tempc - 25) / 3.0 + %s
                       FROM sensor_readings
                       WHERE sensor_id = %s
                         AND rdngtime >= %s
                         AND rdngtime <= %s;''',
                    (factor, factor, factor,
                     factor, factor, factor,
                     factor, factor, factor,
                     factor, factor, factor,
                     int('df', 16),
                     s_id, RDNGTIME_START, RDNGTIME_END))

        for r in cur:
            (rdngtime, rindex, 
             awatthr, bwatthr, cwatthr, 
             avarhr, bvarhr, cvarhr, 
             avahr, bvahr, cvahr, 
             airms, birms, cirms, 
             avrms, bvrms, cvrms, 
             freq, tempc) = r

            data = 'RTSD'
            data += chr(rindex)
            data += chr(awatthr >> 8) + chr(awatthr & 255)
            data += chr(bwatthr >> 8) + chr(bwatthr & 255)
            data += chr(cwatthr >> 8) + chr(cwatthr & 255)
            data += chr(avarhr >> 8) + chr(avarhr & 255)
            data += chr(bvarhr >> 8) + chr(bvarhr & 255)
            data += chr(cvarhr >> 8) + chr(cvarhr & 255)
            data += chr(avahr >> 8) + chr(avahr & 255)
            data += chr(bvahr >> 8) + chr(bvahr & 255)
            data += chr(cvahr >> 8) + chr(cvahr & 255)
            data += (chr(airms >> 16) + chr((airms >> 8) & 255) 
                                      + chr(airms & 255))
            data += (chr(birms >> 16) + chr((birms >> 8) & 255) 
                                      + chr(birms & 255))
            data += (chr(cirms >> 16) + chr((cirms >> 8) & 255) 
                                      + chr(cirms & 255))
            data += (chr(avrms >> 16) + chr((avrms >> 8) & 255) 
                                      + chr(avrms & 255))
            data += (chr(bvrms >> 16) + chr((bvrms >> 8) & 255) 
                                      + chr(bvrms & 255))
            data += (chr(cvrms >> 16) + chr((cvrms >> 8) & 255) 
                                      + chr(cvrms & 255))
            data += chr(freq >> 4) + chr((freq << 4) & 255)
            data += chr(tempc)
            data += chr(0) # TODO

            print '        \'%s\',' % hexlify(data)
        print '    ),'
    print '}'


if __name__ == '__main__':
    main()
