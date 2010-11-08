#!/usr/bin/env python


import psycopg2, sys, time


TABLES = ('AtwoodDorm', 'CaseDorm', 'EastDorm1', 'EastDorm2', 'LindeDorm', 'NorthDorm1', 'NorthDorm2', 'NorthDorm3', 'SontagDorm', 'SouthDorm', 'WestDorm1', 'WestDorm2', 'EastDorm3')


def main(**kwargs):
    conn = psycopg2.connect('dbname=energy user=energy')
    cur = conn.cursor()
    q = 'select '

    for i in range(len(TABLES)):
        q += ''.join(('(select rdngtime as x', str(i), ' from ', TABLES[i], ' order by rdngtime desc limit 1)'))
        if i + 1 == len(TABLES):
            q += ';'
        else:
            q += ', '

    d = [None] * len(TABLES)

    while True:
        cur.execute(q)
        e = cur.fetchone()
        print ''.join([(d[i] != e[i] and '+' or ' ') for i in range(len(TABLES))])
        d = e

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
