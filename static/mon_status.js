$(function () {
    // This function is a callback, called when the DOM is loaded

    var first_time = true;
    var sensor_groups = null;

    function update_cell(name, val, also_label) {
        if ($(name).text() != val) {
            $(name).empty();
            $(name).append(val);
            $(name).animate({ backgroundColor: "#99ee99" }, 400);
            $(name).animate({ backgroundColor: "#ffffff" }, 600);
            if (also_label) {
                $(also_label).animate({ backgroundColor: "#99ee99" }, 400);
                $(also_label).animate({ backgroundColor: "#ffffff" }, 600);
            }
        }
    }

    function refreshdata_json_cb(data) {
        // Given new data from the server, update the page (graph and
        // table).

        // TODO: what if somehow we get no results and it's not the 
        // first time?
        if (first_time && data.no_results) {
            return; // TODO: tell the user what happened?
        }

        // When this function is first called, it is expected that 
        // data_url was defined previously (before loading this file).
        data_url = data.data_url;
        var sensor_id, group_id;

        if (first_time) {
            sensor_groups = data.sensor_groups;

            // When data is received the first time, reveal the table 
            // and remove the graph's loading animation
            $('#monstatus').show();
        }
    
        for (var i=0; i < sensor_groups.length; i++) {
            group_id = sensor_groups[i][0];
    
            for (var j=0; j < sensor_groups[i][3].length; j++) {
                sensor_id = sensor_groups[i][3][j][0];

                if (sensor_id in data.sensor_readings) {
                    update_cell('#last-reading-' + sensor_id, (new Date(data.sensor_readings[sensor_id][0])).toString(), '#sensor-name-' + sensor_id);
                    update_cell('#avg-time-' + sensor_id, data.sensor_readings[sensor_id][1], false);
                    update_cell('#min-time-' + sensor_id, data.sensor_readings[sensor_id][2], false);
                    update_cell('#max-time-' + sensor_id, data.sensor_readings[sensor_id][3], false);
                }
            }
        }
    
        if (first_time) {
            first_time = false;
        }
    
        setTimeout(refreshdata, 2000);
    }
    
    function refreshdata() {
        $.getJSON(data_url, refreshdata_json_cb);
    }

    // Initially, hide the table and show a loading animation instead of
    // the graph
    $('#monstatus').hide();
    refreshdata();
});
