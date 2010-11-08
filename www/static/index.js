function rnd(kw) {
    return kw.toFixed(2);
}

function add_arrays_inplace(a, b) {
    for (var i=0; i < a.length; i++) {
        if (a[i] == null || b[i] == null) {
            a[i] = null;
        } else {
            a[i] += b[i];
        }
    }
}

function epsecs_to_label(es) {
    // Convert seconds since the epoch to a human-friendly time string
    var d = new Date(1000 * es);
    var hrs = (d.getHours() - 1) % 12 + 1;
    var ampm = ((d.getHours() >= 12) ? 'pm' : 'am');
    var mins = d.getMinutes();
    mins = (mins < 10 ? '0' + mins : mins);
    return (hrs + ':' + mins + ' ' + ampm);
}

function refreshdata(first_time) {
    /* Call the server, get new data, and update the page.  If first_time
     * is true, retrieve all data needed for the page.  Otherwise, use
     * data stored from last time and only retrieve the delta.
     *
     * If we ask for data123456789.js, we will get the data since timestamp
     * 123456789 (seconds since epoch).
     */
    var f = 'data';
    if (! first_time) {
        f = f + $prev_x[$prev_x.length - 1];
    }
    f = f + '.js'
    $.getJSON(f, function(data) {
        var y = [];
        var x = [];
        var series_opts = [];
        var sg_inds = [];
        var sgs, grp_week_avg, grp_month_avg, sensor_id, ind, all_data_x;
        var sensor_structure, sensors, sensor_groups
        if (first_time) {
            all_data_x = data.x;
            sensor_structure = data.sensor_structure;
            sensors = data.sensors;
            sensor_groups = data.sensor_groups;
        } else {
            /* We've already collected some data, so combine it with the new.
             * A word on this slicing:  We're discarding our latest record,
             * preferring the new copy from the sever, since last time we may 
             * have e.g. collected data just before a sensor reported a 
             * reading (for the 10-second time period we were considering).
             * Hence, the second latest and older records are always safe---
             * they will /never/ change.
             */
            all_data_x = $prev_x.slice(data.x.length - 1, 
                                       $prev_x.length - 1).concat(data.x);
            sensor_structure = $prev_sensor_structure;
            sensors = $prev_sensors;
            sensor_groups = $prev_sensor_groups;
        }
        // We will pass x to the grapher
        var tick_interval = Math.floor(all_data_x.length / 10.0);
        for (var i=0; i < all_data_x.length; i += tick_interval) {
            x[x.length] = [i+1, epsecs_to_label(all_data_x[i])];
        }
        // Now organize y values and update the table averages all at once
        // for i in sensor groups...
        for (var i=0; i < sensor_structure.length; i++) {
            sgs = sensor_structure[i];
            grp_week_avg = 0;
            grp_month_avg = 0;
            // for j in sensors within the group...
            for (var j=0; j < sgs[1].length; j++) {
                sensor_id = sgs[1][j];
                // update the per-sensor table averages, if appropriate
                if (sgs[1].length > 1) {
                    $('#WeeklyS' + sensor_id).empty();
                    $('#WeeklyS' + sensor_id).append(rnd(
                        data.week_averages[sensor_id]));
                    $('#MonthlyS' + sensor_id).empty();
                    $('#MonthlyS' + sensor_id).append(rnd(
                        data.month_averages[sensor_id]));
                }
                ind = sg_inds.indexOf(sgs[0]);
                if (ind < 0) {
                    // we didn't haven't looked at this sensor group before
                    y[y.length] = data.y[sensor_id];
                    sg_inds[sg_inds.length] = sgs[0];
                    series_opts[series_opts.length] = {
                        label: sensor_groups[sgs[0]][0],
                        color: '#' + sensor_groups[sgs[0]][1]
                    };
                } else {
                    /* We've already processed data for this sensor.
                     * Combine the two arrays by adding by-element.
                     */
                    add_arrays_inplace(y[ind], data.y[sensor_id]);
                }
                grp_week_avg += data.week_averages[sensor_id];
                grp_month_avg += data.month_averages[sensor_id];
            }
            // Now update table averages for this sensor /group/
            if (sgs[1].length > 1) {
                $('#WeeklySG' + sgs[0]).empty();
                $('#WeeklySG' + sgs[0]).append(rnd(grp_week_avg));
                $('#MonthlySG' + sgs[0]).empty();
                $('#MonthlySG' + sgs[0]).append(rnd(grp_month_avg));
            } else {
                $('#WeeklySG' + sgs[0]).empty();
                $('#WeeklySG' + sgs[0]).append(rnd(
                    data.week_averages[sensor_id]));
                $('#MonthlySG' + sgs[0]).empty();
                $('#MonthlySG' + sgs[0]).append(
                    rnd(data.month_averages[sensor_id]));
            }
        }
        if (! first_time) {
            for (var j=0; j < $prev_y.length; j++) {
                /* As before, we combine old data with the new, discarding
                 * our last element for the new calculation provided by the 
                 * server.
                 */
                y[j] = $prev_y[j].slice(y[j].length - 1, 
                                        $prev_y[j].length - 1).concat(y[j]);
            }
        }
        // Finally, make the graph
        $('#graph').empty();
        $.jqplot('graph', y, {
            seriesDefaults: {
                showMarker: false
            },
            series: series_opts,
            legend: {
                show: true,
                location: 'ne',
                placement: 'outsideGrid',
                textColor: 'black',
                fontSize: '16px',
                fontFamily: 'sans-serif'

            },
            title: {
                text: 'Real-Time Power Consumption at Mudd',
                textColor: 'black',
                fontSize: '18px',
                fontFamily: 'sans-serif'
            },
            axes: {
                xaxis: {
                    ticks: x,
                    tickOptions: {
                        textColor: 'black',
                        fontSize: '16px',
                        fontFamily: 'sans-serif'
                    }
                },
                yaxis: {
                    label: '(kW)',
                    labelOptions: {
                        textColor: 'black',
                        fontSize: '16px',
                        fontFamily: 'sans-serif'
                    },
                    tickOptions: {
                        textColor: 'black',
                        fontSize: '16px',
                        fontFamily: 'sans-serif'
                    }
                }
            }
        });
        /* Store all data for the next iteration and set the timer.
         * (This procedure can probably be improved considerably.)
         */
        $prev_x = all_data_x;
        $prev_y = y;
        $prev_sgs = sgs;
        $prev_sensors = sensors;
        $prev_sensor_groups = sensor_groups;
        $prev_sensor_structure = sensor_structure;
        setTimeout("refreshdata(false)", 10000);
    });
}