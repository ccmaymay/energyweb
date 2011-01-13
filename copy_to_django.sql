insert into graph_sensorgroup (name, color) select name, color from sensor_groups order by id asc;
insert into graph_sensor (name, ip, sensor_group_id, three_phase, factor, port) select name, ip, sensor_group_id, three_phase, factor, port from sensors order by id asc;
insert into graph_poweraverage (first_reading_time, last_reading_time, trunc_reading_time, sensor_id, num_points, watts, average_type) select rdngtime_first, rdngtime_last, rdngtime_trunc, sensor_id, num_pts, watts, avg_type from power_averages;
insert into graph_sensorreading (sensor_id, reading_time, rindex, awatthr, bwatthr, cwatthr, avarhr, bvarhr, cvarhr, avahr, bvahr, cvahr, airms, birms, cirms, avrms, bvrms, cvrms, tempc, freq) select sensor_id, rdngtime, rindex, awatthr, bwatthr, cwatthr, avarhr, bvarhr, cvarhr, avahr, bvahr, cvahr, airms, birms, cirms, avrms, bvrms, cvrms, tempc, freq from sensor_readings;
