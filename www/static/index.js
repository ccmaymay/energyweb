$(function () {
    // This function is a callback, called when the DOM is loaded

    var first_time = true;
    var prev_last_record = null;
    var prev_y = null;
    var prev_sgs = null;
    var prev_sensors = null;
    var prev_sensor_groups = null;
    var prev_sensor_structure = null;

    function array_index_of(ar, x) {
        // (IE doesn't have Array.indexOf)
        for (var i=0; i < ar.length; i++) {
            if (ar[i] == x) {
                return i;
            }
        }
        return -1;
    }
    
    function rnd(x) {
        return x.toFixed(2);
    }
    
    function refreshdata_json_cb(data) {
        // Given new data from the server, update the page (graph and
        // table).
    
        var y = [];
        var series_opts = [];
        var missed_week_average, missed_month_average;
        var sgs, grp_week_avg, grp_month_avg, sensor_id;
        var sensor_structure, sensors, sensor_groups, graph_opts; 
        if (first_time) {
            sensor_structure = data.sensor_structure;
            sensors = data.sensors;
            sensor_groups = data.sensor_groups;
        } else {
            sensor_structure = prev_sensor_structure;
            sensors = prev_sensors;
            sensor_groups = prev_sensor_groups;
        }
    
        series = [];
    
        // for i in sensor groups...
        for (var i=0; i < sensor_structure.length; i++) {
            // sgs now corresponds to the array representing to the
            // first sensor group in sensor_structure
            sgs = sensor_structure[i];
            sensor_group_id = sgs[0];
            grp_week_avg = 0;
            grp_month_avg = 0;
            missed_week_average = false;
            missed_month_average = false;
    
            if (first_time) {
                y[sensor_group_id] = data.y[sensor_group_id];
            } else {
                /* We've already collected some data, so combine it with the 
                 * new.  A word on this slicing:  We're discarding our latest 
                 * record, preferring the new copy from the sever, since last 
                 * time we may have e.g. collected data just before a sensor 
                 * reported a reading (for the 10-second time period we were 
                 * considering).  Hence, the second latest and older records 
                 * are always safe---they will /never/ change.
                 */
                y[sensor_group_id] = prev_y[sensor_group_id].slice(
                    data.y[sensor_group_id].length - 1, 
                    prev_y[sensor_group_id].length - 1).concat(
                    data.y[sensor_group_id]);
            }
            
            series.push({
                data: y[sensor_group_id],
                label: sensor_groups[sensor_group_id][0],
                color: '#' + sensor_groups[sensor_group_id][1]
            });
    
            // for j in sensors within the group...
            for (var j=0; j < sgs[1].length; j++) {
                sensor_id = sgs[1][j];
    
                // update the per-sensor table averages, if appropriate
                if (sgs[1].length > 1) {
                    if (sensor_id in data.week_averages) {
                        $('#WeeklyS' + sensor_id).empty();
                        $('#WeeklyS' + sensor_id).append(rnd(
                            data.week_averages[sensor_id]));
                    } else {
                        missed_week_average = true;
                    }
                    if (sensor_id in data.month_averages) {
                        $('#MonthlyS' + sensor_id).empty();
                        $('#MonthlyS' + sensor_id).append(rnd(
                            data.month_averages[sensor_id]));
                    } else {
                        missed_month_average = true;
                    }
                }
    
                // Add sensor averages to the sensor group averages...
                if (sensor_id in data.week_averages) {
                    grp_week_avg += data.week_averages[sensor_id];
                }
                if (sensor_id in data.month_averages) {
                    grp_month_avg += data.month_averages[sensor_id];
                }
            }
    
            // Now update table averages for this sensor group
            if (! missed_week_average) {
                $('#WeeklySG' + sensor_group_id).empty();
                $('#WeeklySG' + sensor_group_id).append(rnd(grp_week_avg));
            }
            if (! missed_month_average) {
                $('#MonthlySG' + sensor_group_id).empty();
                $('#MonthlySG' + sensor_group_id).append(rnd(grp_month_avg));
            }
        }
        // Finally, make the graph
        graph_opts = {
            series: {
                lines: {show: true},
                points: {show: false}
            },
            legend: {
                show: true,
                position: 'ne',
                backgroundOpacity: 0.6,
                noColumns: sensor_structure.length
            },
            yaxis: {
                min: 0
            },
            xaxis: {
                mode: 'time',
                timeformat: '%h:%M %p',
                twelveHourClock: true
            },
            grid: {
                show: true,
                color: '#d0d0d0',
                borderColor: '#bbbbbb',
                backgroundColor: { colors: ['#dbefff', '#ffffff']}
            }
        };
        $.plot($('#graph'), series, graph_opts);
    
        // Store all data for the next iteration and set the timer.
        prev_last_record = data.last_record;
        prev_y = y;
        prev_sgs = sgs;
        prev_sensors = sensors;
        prev_sensor_groups = sensor_groups;
        prev_sensor_structure = sensor_structure;
    
        if (first_time) {
            first_time = false;
        }
    
        setTimeout(refreshdata, 10000);
    }
    
    function refreshdata() {
        /* Call the server, get new data, and update the page.  If first_time
         * is true, retrieve all data needed for the page.  Otherwise, use
         * data stored from last time and only retrieve the delta.
         *
         * If we ask for data123456789.json, we will get the data since 
         * timestamp 123456789 (seconds since epoch, UTC).
         */
        var f = 'data';
        if (! first_time) {
            f = f + prev_last_record;
        }
        f = f + '.json'
    
        $.getJSON(f, refreshdata_json_cb);
    }

    refreshdata();
});
