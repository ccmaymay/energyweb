-- Copy data from energyweb 0.3 to a Django-initialized database of
-- energyweb 0.4.

-- NOTE: This has not been tested with the latest version.  Use with 
-- care.

INSERT INTO graph_sensorgroup 
  (name, color) 
  SELECT name, color 
  FROM sensor_groups ORDER BY id ASC;
INSERT INTO graph_sensor 
  (name, ip, sensor_group_id, three_phase, factor, port) 
  SELECT name, ip, sensor_group_id, three_phase, factor, port 
  FROM sensors ORDER BY id ASC;
-- TODO:
-- Check that the script that generates power averages comes up with
-- the same answers as those in power_averages?
INSERT INTO graph_poweraverage 
  (first_reading_time, last_reading_time, trunc_reading_time, sensor_id, 
  num_points, watts, average_type) 
  SELECT rdngtime_first, rdngtime_last, rdngtime_trunc, sensor_id, 
  num_pts, watts, avg_type 
  FROM power_averages;
INSERT INTO graph_sensorreading 
  (sensor_id, reading_time, rindex, 
  awatthr, bwatthr, cwatthr, 
  avarhr, bvarhr, cvarhr, 
  avahr, bvahr, cvahr, 
  airms, birms, cirms, 
  avrms, bvrms, cvrms, 
  tempc, freq) 
  SELECT sensor_id, rdngtime, rindex, 
  awatthr, bwatthr, cwatthr, 
  avarhr, bvarhr, cvarhr, 
  avahr, bvahr, cvahr, 
  airms, birms, cirms, 
  avrms, bvrms, cvrms, 
  tempc, freq 
  FROM sensor_readings;
