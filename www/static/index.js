$(function () {
    // This function is a callback, called when the DOM is loaded

    var first_time = true;
    var last_record = null;
    var sg_xy_pairs = {};
    var sensor_groups = null;

    function kw_tickformatter(val, axis) {
        // Workaround to get units on the y axis
        return val + " kW";
    }
    
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
        // (Used to format numbers in the table)
        return x.toFixed(2);
    }
    
    function refreshdata_json_cb(data) {
        // Given new data from the server, update the page (graph and
        // table).
    
        last_record = data.last_record;

        var series_opts = [];
        var series = [];
        var missed_week_average, 
            missed_month_average, 
            sensor_id,
            group_week_avg, 
            group_month_avg, 
            graph_opts;

        if (first_time) {
            sensor_groups = data.sensor_groups;

            // When data is received the first time, reveal the table 
            // and remove the graph's loading animation
            $('#energystats').show();
            $('#graph').empty();
        }
    
        for (var i=0; i < sensor_groups.length; i++) {
            group_week_avg = 0;
            group_month_avg = 0;
            missed_week_average = false;
            missed_month_average = false;
    
            if (first_time) {
                sg_xy_pairs[sensor_groups[i][0]] = data.sg_xy_pairs[
                    sensor_groups[i][0]];
            } else {
                /* We've already collected some data, so combine it 
                 * with the new.  About this slicing:  We're 
                 * discarding our latest record, preferring the new copy
                 * from the sever, since last time we may have e.g. 
                 * collected data just before a sensor reported a 
                 * reading (for the 10-second time period we were 
                 * considering).  Hence, while the latest record may be
                 * incomplete, the second latest (and older) records are
                 * safe---they will never change.
                 */
                sg_xy_pairs[sensor_groups[i][0]] = sg_xy_pairs[
                    sensor_groups[i][0]].slice(
                        data.sg_xy_pairs[sensor_groups[i][0]].length 
                            - 1,
                        sg_xy_pairs[sensor_groups[i][0]].length - 1
                    ).concat(
                        data.sg_xy_pairs[sensor_groups[i][0]]);
            }
            
            series.push({
                data: sg_xy_pairs[sensor_groups[i][0]],
                label: sensor_groups[i][1],
                color: '#' + sensor_groups[i][2]
            });
    
            for (var j=0; j < sensor_groups[i][3].length; j++) {
                sensor_id = sensor_groups[i][3][j][0];

                // update the per-sensor table averages, if appropriate
                if (sensor_groups[i][3].length > 1) {
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
                    group_week_avg += data.week_averages[sensor_id];
                }
                if (sensor_id in data.month_averages) {
                    group_month_avg += data.month_averages[sensor_id];
                }
            }
    
            // Now update table averages for this sensor group
            if (! missed_week_average) {
                $('#WeeklySG' + sensor_groups[i][0]).empty();
                $('#WeeklySG' + sensor_groups[i][0]).append(
                    rnd(group_week_avg));
            }
            if (! missed_month_average) {
                $('#MonthlySG' + sensor_groups[i][0]).empty();
                $('#MonthlySG' + sensor_groups[i][0]).append(
                    rnd(group_month_avg));
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
                noColumns: sensor_groups.length
            },
            yaxis: {
                min: 0,
                tickFormatter: kw_tickformatter,
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
    
        if (first_time) {
            first_time = false;
        }
    
        setTimeout(refreshdata, 10000);
    }
    
    function refreshdata() {
        /* Call the server, get new data, and update the page.  If 
         * first_time is true, retrieve all data needed for the page.  
         * Otherwise, use data stored from last time and only retrieve
         * the delta.
         
         * If we ask for data123456789.json, we will get the data since
         * timestamp 123456789 (seconds since epoch, UTC).
         */
        var f = 'data';
        if (! first_time) {
            f = f + last_record;
        }
        // the (new Date()).getTime() is just to prevent caching
        f = f + '-' + (new Date()).getTime() + '.json';
    
        $.getJSON(f, refreshdata_json_cb);
    }

    // Initially, hide the table and show a loading animation instead of
    // the graph
    $('#energystats').hide();
    $('#graph').append(
        '<img class="loading" src="static/loading.gif" />');
    refreshdata();
});
