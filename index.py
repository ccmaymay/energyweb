import psycopg2, datetime

page_html = '''
<html>
<head>
    <title>WEB Distributed Wireless Electric Utility Monitoring</title>
</head>
<body>
    <table>
        <tr>
            <td>Dorm</td>
            <td>Atwood</td>
            <td>Case</td>
            <td>East</td>
            <td>Linde</td>
            <td>North</td>
            <td>Sontag</td>
            <td>South</td>
            <td>West</td>
        </tr>
        <tr>
            <td>Last 24 Hours</td>
            <td>Atwood</td>
            <td>Case</td>
            <td>East</td>
            <td>Linde</td>
            <td>North</td>
            <td>Sontag</td>
            <td>South</td>
            <td>West</td>
        </tr>
        <tr>
            <td>Avg kW since TODO (last date entered)</td>
            <td>%f</td>
            <td>%f</td>
            <td>%f</td>
            <td>%f</td>
            <td>%f</td>
            <td>%f</td>
            <td>%f</td>
            <td>%f</td>
        </tr>
    </table>
</body>
</html>'''

def main():
    conn = psycopg2.connect('dbname=rhizome user=rhizome')
    cur = conn.cursor()

    cur.execute(select_stmt)
    tup = cur.fetchone()

    cur.close()
    conn.close()

    'SELECT .01*(SUM(c3) + SUM(c4) + SUM(c5)) /(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from AtwoodDorm where now() - c1 <= interval \'24 hours\') as atwooddorm_cut'
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from CaseDorm where now() - c1 <= interval \'24 hours\') as casedorm_cut'
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from LindeDorm where now() - c1 <= interval \'24 hours\') as lindedorm_cut'
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from SontagDorm where now() - c1 <= interval \'24 hours\') as sontagdorm_cut'
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from NorthDorm1 where now() - c1 <= interval \'24 hours\') as northdorm1_cut'
    'SELECT .01*(SUM(c3)+SUM(c4))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4 from NorthDorm2 where now() - c1 <= interval \'24 hours\') as northdorm2_cut'
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from NorthDorm3 where now() - c1 <= interval \'24 hours\') as northdorm3_cut'
    #Total = sum of last three
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from EastDorm1 where now() - c1 <= interval \'24 hours\') as eastdorm1_cut'
    'SELECT .01*(SUM(c3)+SUM(c4))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4 from EastDorm2 where now() - c1 <= interval \'24 hours\') as eastdorm2_cut'
    #Total = sum of last TWO, except incl c5... (east3 for south)
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from EastDorm3 where now() - c1 <= interval \'24 hours\') as eastdorm3_cut'
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from WestDorm1 where now() - c1 <= interval \'24 hours\') as westdorm1_cut'
    'SELECT .01*(SUM(c3)+SUM(c4))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4 from WestDorm2 where now() - c1 <= interval \'24 hours\') as westdorm2_cut'
    #Total = sum of last two, except incl c5, AND east3 (??)
    'SELECT .01*(SUM(c3)+SUM(c4)+SUM(c5))/(extract(epoch from max(c1)) - extract(epoch from min(c1))) FROM (SELECT c1, c3, c4, c5 from SouthDorm where now() - c1 <= interval \'24 hours\') as southdorm_cut'
    
    title_text = 'Watts last 4 hours'
    x_axis_text = 'time'
    y_axis_text = 'power (kW)'
    #x = c1
    #y = expr1 = (c3 + c4 + c5) / 1000, or (c3 + c4) / 1000 for east2, north2, west2
