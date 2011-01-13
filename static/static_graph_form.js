$(function () {
    // This function is a callback, called when the DOM is loaded
    $('#id_start_0').datepicker({ dateFormat: 'yy-mm-dd' });
    $('#id_end_0').datepicker({ dateFormat: 'yy-mm-dd' });
    $('#id_start_1').timepicker({ showPeriod: true, showLeadingZero: false });
    $('#id_end_1').timepicker({ showPeriod: true, showLeadingZero: false });
});
