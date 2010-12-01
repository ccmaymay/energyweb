SELECT sensor_groups.name AS dorm, 
       ROUND(CAST (SUM(power_averages.watts / 1000) AS numeric), 3) AS kW, 
       MIN(power_averages.rdngtime_first) AS first_record, 
       MAX(power_averages.rdngtime_last) AS last_record,
       SUM(num_pts) AS num_data_points
  FROM power_averages 
    INNER JOIN sensors ON (power_averages.sensor_id = sensors.id) 
    INNER JOIN sensor_groups on (sensors.sensor_group_id = sensor_groups.id) 
  WHERE power_averages.avg_type = 2 
    AND power_averages.rdngtime_first >= '2010-11-01 00:00:00' 
    AND power_averages.rdngtime_first < '2010-12-01 00:00:00'
  GROUP BY sensor_groups.name 
  ORDER BY sensor_groups.name ASC;
