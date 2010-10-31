function rnd(kw) {
    return kw.toFixed(2);
}

function refreshdata() {
    document.getElementById('energygraph').src = 'energygraph.png?' + Date.parse(new Date().toString());
    $.getJSON('energystats.js', function(data) {
        ab = new Date(1000 * data.ApproxBeginning);
        $('#approxbegin').empty();
        hrs = (ab.getHours() - 1) % 12 + 1;
        ampm = ((ab.getHours() >= 12) ? 'pm' : 'am');
        $('#approxbegin').append(ab.getMonth()
                                 + '/' + ab.getDate()
                                 + '/' + ab.getFullYear()
                                 + ' ' + hrs
                                 + ':' + ab.getMinutes()
                                 + ' ' + ampm);

        $('#Atwood24hr').empty();
        $('#Atwood24hr').append(rnd(data.Atwood[0]));
        $('#AtwoodTot').empty();
        $('#AtwoodTot').append(rnd(data.Atwood[1]));

        $('#Case24hr').empty();
        $('#Case24hr').append(rnd(data.Case[0]));
        $('#CaseTot').empty();
        $('#CaseTot').append(rnd(data.Case[1]));

        $('#East24hr').empty();
        $('#East24hr').append(rnd(data.East[0]));
        $('#EastTot').empty();
        $('#EastTot').append(rnd(data.East[1]));

        $('#Linde24hr').empty();
        $('#Linde24hr').append(rnd(data.Linde[0]));
        $('#LindeTot').empty();
        $('#LindeTot').append(rnd(data.Linde[1]));

        $('#North24hr').empty();
        $('#North24hr').append(rnd(data.North[0]));
        $('#NorthTot').empty();
        $('#NorthTot').append(rnd(data.North[1]));

        $('#Sontag24hr').empty();
        $('#Sontag24hr').append(rnd(data.Sontag[0]));
        $('#SontagTot').empty();
        $('#SontagTot').append(rnd(data.Sontag[1]));

        $('#South24hr').empty();
        $('#South24hr').append(rnd(data.South[0]));
        $('#SouthTot').empty();
        $('#SouthTot').append(rnd(data.South[1]));

        $('#West24hr').empty();
        $('#West24hr').append(rnd(data.West[0]));
        $('#WestTot').empty();
        $('#WestTot').append(rnd(data.West[1]));
    });
    setTimeout("refreshdata()", 10000);
}
