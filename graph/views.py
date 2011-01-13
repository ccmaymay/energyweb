# Create your views here.
from django.shortcuts import render_to_response
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django import forms
from graph.models import SensorGroup, Sensor, PowerAverage
import calendar, datetime, simplejson


STATIC_GRAPH_RESS = [res for res in PowerAverage.AVERAGE_TYPES
                              if res != 'month'] # TODO
STATIC_GRAPH_RES_CHOICES = ([('auto', 'auto')]
    + [(res_choice, PowerAverage.AVERAGE_TYPE_DESCRIPTIONS[res_choice])
       for res_choice in STATIC_GRAPH_RESS])

DATE_INPUT_FORMATS = (
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y',              # '10/25/06'
)

TIME_INPUT_FORMATS = (
    '%H:%M',        # '14:30'
    '%I:%M %p',     # '2:30 PM'
    '%I%p',         # '2PM'
)

# If a full graph has this many points or fewer, show the individual
# points.  (Otherwise only draw the lines.)
GRAPH_SHOW_POINTS_THRESHOLD = 40


class StaticGraphForm(forms.Form):
    _DATE_FORMAT = '%Y-%m-%d'
    _TIME_FORMAT = '%l:%M %p'
    _DT_INPUT_SIZE = '10'

    start = forms.SplitDateTimeField(input_date_formats=DATE_INPUT_FORMATS,
        input_time_formats=TIME_INPUT_FORMATS,
        widget=forms.SplitDateTimeWidget(attrs={'size': _DT_INPUT_SIZE},
                                         date_format=_DATE_FORMAT,
                                         time_format=_TIME_FORMAT))

    end = forms.SplitDateTimeField(input_date_formats=DATE_INPUT_FORMATS,
        input_time_formats=TIME_INPUT_FORMATS,
        widget=forms.SplitDateTimeWidget(attrs={'size': _DT_INPUT_SIZE},
                                         date_format=_DATE_FORMAT,
                                         time_format=_TIME_FORMAT))

    res = forms.ChoiceField(label='Resolution', 
        choices=STATIC_GRAPH_RES_CHOICES)


def _get_sensor_groups():
    return [[sg.pk, sg.name, sg.color, 
             [[s.pk, s.name] 
              for s in sg.sensor_set.all()]] 
            for sg in SensorGroup.objects.all()]


def data_interface(request):
    return render_to_response('graph/data_interface.html', 
        {'interface_url_template': 
             '/graph/static/<start>/to/<end>/<res>/data.json',
         'interface_start_placeholder': '<start>',
         'interface_end_placeholder': '<end>',
         'interface_res_placeholder': '<res>',
         'interface_junk_suffix': '?junk=<junk>',
         'interface_junk_placeholder': '<junk>',
         'res_choices': STATIC_GRAPH_RES_CHOICES},
        context_instance=RequestContext(request))


def index(request):
    junk = str(calendar.timegm(datetime.datetime.now().timetuple()))
    start_dt = datetime.datetime.now() - datetime.timedelta(0, 3600*3, 0)
    data = str(int(calendar.timegm(start_dt.timetuple()) * 1000))
    return render_to_response('graph/index.html', 
        {'sensor_groups': SensorGroup.objects.all(),
         'data_url': reverse('graph.views.index_data', 
                             kwargs={'data': data}) + '?junk=' + junk},
        context_instance=RequestContext(request))


def index_data(request, data):
    from django.db import connection, transaction
    cur = connection.cursor()

    sensor_groups = SensorGroup.objects.all()
    sensor_ids_by_group = {}
    sensor_ids = []
    for sg in sensor_groups:
        sensor_id_set = [s.pk for s in sg.sensor_set.all()]
        sensor_ids_by_group[sg.pk] = sensor_id_set
        sensor_ids.extend(sensor_id_set)

    # We will display only the latest averages for the user, so
    # assume the latest average is calculated for each sensor 
    # (within a given average type).  If some averages have not
    # been computed---so our query returns several of the latest
    # time-period averages, but also some averages from the past,
    # and hence does not contain the latest averages for all
    # sensors---then return None in their place.

    week_and_month_averages = dict(week={}, month={})

    for average_type in ('week', 'month'):
        trunc_reading_time = None
        for average in PowerAverage.objects.filter(average_type=average_type
            ).order_by('-trunc_reading_time')[:len(sensor_ids)]:

            if trunc_reading_time is None:
                trunc_reading_time = average.trunc_reading_time
            if average.trunc_reading_time == trunc_reading_time:
                week_and_month_averages[average_type][average.sensor_id] \
                    = average.watts / 1000.0
        for sensor_id in sensor_ids:
            if not week_and_month_averages[average_type].has_key(sensor_id):
                week_and_month_averages[average_type][sensor_id] = None

    week_averages = week_and_month_averages['week']
    month_averages = week_and_month_averages['month']

    # Now, calculate the data points for the graph we're going to
    # display.  This is harder than it should be since the points
    # are pulled from a practically continuous range of times,
    # but we want to somehow sum the lines within a given sensor
    # group---we want West Dorm's power usage, not the usages on
    # West's three individual sensors.  Stochastic simulation (e.g.)
    # may have something very interesting to say about this, but for
    # the time being we will settle for summing points within
    # ten-second intervals.  The client (javascript) can then deal
    # with the null values (the infrequent cases when no reading
    # appears within one of these 10-second bins for a certain
    # sensor) as it desires.  (3 hours, by the way, is the length of
    # time to be represented on the graph.)

    # trunc_reading_time in the query below is a timestamp representing
    # the ten-second interval to which the current reading belongs.

    # If the client has supplied data (a string of digits in the
    # URL---representing UTC seconds since the epoch), then we only
    # consider data since (and including) that timestamp.

    # The max is here just in case a client accidentally calls this
    # view with a weeks-old timestamp...
    start_dt = max(datetime.datetime.utcfromtimestamp(int(data) / 1000),
                   datetime.datetime.now() - datetime.timedelta(0, 3600*3, 0))
    PowerAverage.graph_data_execute(cur, 'second*10', start_dt)

    # Also note, above, that if data was supplied then we selected
    # everything since the provided timestamp's truncated date,
    # including that date.  We will always provide the client with
    # a new copy of the latest record he received last time, since
    # that last record may have changed (more sensors may have
    # submitted measurements and added to it).  The second to
    # latest and older records, however, will never change.

    # Now organize the query in a format amenable to the 
    # (javascript) client.  (The grapher wants (x, y) pairs.)

    sg_xy_pairs = dict([[sg.pk, []] for sg in sensor_groups])
    r = cur.fetchone()
    if r is None:
        d = {'no_results': True,
             'week_averages': week_and_month_averages['week'],
             'month_averages': week_and_month_averages['month']}
    else:
        per = r[2]
        per_incr = datetime.timedelta(0, 10, 0)
    
        # At the end of each outer loop, we increment per (the current
        # ten-second period of time we're considering) by ten seconds.
        while r is not None:
            # Remember that the JavaScript client takes (and
            # gives) UTC timestamps in ms
            x = int(calendar.timegm(per.timetuple()) * 1000)
            for sg in sensor_groups:
                y = 0
                for sid in sensor_ids_by_group[sg.pk]:
                    # If this sensor has a reading for the current per,
                    # update y.  There are three ways the sensor might
                    # not have such a reading:
                    # 1. r is None, i.e. there are no more readings at
                    #    all
                    # 2. r is not None and r[2] > per, i.e. there are 
                    #    more readings but not for this per
                    # 3. r is not None and r[2] <= per and r[1] != s[0],
                    #    i.e. there are more readings for this per,
                    #    but none for this sensor
                    if r is not None and r[2] <= per and r[1] == sid:
                        # If y is None, leave it as such.   Else, add
                        # this sensor reading to y.  Afterwards, in
                        # either case, fetch a new row.
                        if y is not None:
                            y += float(r[0])
                        r = cur.fetchone()
                    else:
                        y = None
                sg_xy_pairs[sg.pk].append((x, y))
            per += per_incr
    
        last_record = x
        # desired_first_record lags by (3:00:00 - 0:00:10) = 2:59:50
        desired_first_record = x - 1000*3600*3 + 1000*10
    
        junk = str(calendar.timegm(datetime.datetime.now().timetuple()))
        data_url = reverse('graph.views.index_data', 
                           kwargs={'data': str(last_record)}) + '?junk=' + junk
        d = {'no_results': False,
             'sg_xy_pairs': sg_xy_pairs,
             'desired_first_record':
                 desired_first_record,
             'week_averages': week_and_month_averages['week'],
             'month_averages': week_and_month_averages['month'],
             'sensor_groups': _get_sensor_groups(),
             'data_url': data_url}

    json_serializer = serializers.get_serializer("json")()
    return HttpResponse(#TODO json_serializer.serialize(d, ensure_ascii=False),
                        simplejson.dumps(d),
                        mimetype='application/json')


def static_graph(request):
    if (request.method == 'GET' 
        and 'start_0' in request.GET 
        and 'end_0' in request.GET 
        and 'res' in request.GET):

        # Allow user to have inputted e.g. pm or p.m. instead of PM
        _get = request.GET.copy()
        _get['start_1'] = _get['start_1'].upper().replace('.', '')
        _get['end_1'] = _get['end_1'].upper().replace('.', '')

        form = StaticGraphForm(_get)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            res = form.cleaned_data['res']
            delta = end - start
            if res not in STATIC_GRAPH_RESS:
                if delta.days > 7*52*3: # 3 years
                    res = 'week'
                elif delta.days > 7*8: # 8 weeks
                    res = 'day'
                elif delta.days > 6:
                    res = 'hour'
                elif delta.days > 0:
                    res = 'minute*10'
                elif delta.seconds > 3600*3: # 3 hours
                    res = 'minute'
                else:
                    res = 'second*10'

            int_start = int(calendar.timegm(start.timetuple()))
            int_end = int(calendar.timegm(end.timetuple()))
            js_start = int_start * 1000
            js_end = int_end * 1000
            junk = str(calendar.timegm(datetime.datetime.now().timetuple()))

            data_url = reverse('graph.views.static_graph_data',
                               kwargs={'start': str(int_start), 
                                       'end': str(int_end), 
                                       'res': res}) + '?junk=' + junk

            return render_to_response('graph/static_graph.html', 
                {'sensor_groups': SensorGroup.objects.all(),
                 'start': js_start,
                 'end': js_end,
                 'data_url': data_url,
                 'form': form,
                 'form_action': reverse('graph.views.static_graph'),
                 'res': res},
                context_instance=RequestContext(request))

        return render_to_response('graph/static_graph_form.html',
            {'form_action': reverse('graph.views.static_graph'),
             'form': form},
            context_instance=RequestContext(request))

    else:
        now = datetime.datetime.now()
        one_day_ago = now - datetime.timedelta(1)
        form = StaticGraphForm(initial={
            'start': one_day_ago,
            'end': now
        })
        return render_to_response('graph/static_graph_form.html',
            {'form_action': reverse('graph.views.static_graph'),
             'form': form},
            context_instance=RequestContext(request))


def static_graph_data(request, start, end, res):
    from django.db import connection, transaction
    cur = connection.cursor()

    start_dt = datetime.datetime.utcfromtimestamp(int(start))
    end_dt = datetime.datetime.utcfromtimestamp(int(end))
    delta = end_dt - start_dt
    per_incr = PowerAverage.AVERAGE_TYPE_TIMEDELTAS[res]
    max_points = ((delta.days * 3600 * 24 + delta.seconds) 
                  / float(per_incr.days * 3600 * 24 + per_incr.seconds))

    sensor_groups = SensorGroup.objects.all()
    sensor_ids_by_group = {}
    sensor_ids = []
    for sg in sensor_groups:
        sensor_id_set = [s.pk for s in sg.sensor_set.all()]
        sensor_ids_by_group[sg.pk] = sensor_id_set
        sensor_ids.extend(sensor_id_set)

    # Now, calculate the data points for the graph we're going to
    # display.  This is harder than it should be since the points
    # are pulled from a practically continuous range of times,
    # but we want to somehow sum the lines within a given sensor
    # group---we want West Dorm's power usage, not the usages on
    # West's three individual sensors.  Stochastic simulation (e.g.)
    # may have something very interesting to say about this, but for
    # the time being we will settle for summing points within
    # ten-second intervals.  The client (javascript) can then deal
    # with the null values (the infrequent cases when no reading
    # appears within one of these 10-second bins for a certain
    # sensor) as it desires.  (3 hours, by the way, is the length of
    # time to be represented on the graph.)

    # trunc_reading_time in the query below is a timestamp representing
    # the ten-second interval to which the current reading belongs.

    # If the client has supplied data (a string of digits in the
    # URL---representing UTC seconds since the epoch), then we only
    # consider data since (and including) that timestamp.

    PowerAverage.graph_data_execute(cur, res, start_dt, end_dt)

    # Also note, above, that if data was supplied then we selected
    # everything since the provided timestamp's truncated date,
    # including that date.  We will always provide the client with
    # a new copy of the latest record he received last time, since
    # that last record may have changed (more sensors may have
    # submitted measurements and added to it).  The second to
    # latest and older records, however, will never change.

    # Now organize the query in a format amenable to the 
    # (javascript) client.  (The grapher wants (x, y) pairs.)

    sg_xy_pairs = dict([[sg.pk, []] for sg in sensor_groups])
    r = cur.fetchone()
    if r is None:
        d = {'no_results': True,
             'sensor_groups': _get_sensor_groups()}
    else:
        per = r[2]

        # At the end of each outer loop, we increment per (the current
        # ten-second period of time we're considering) by ten seconds.
        while r is not None:
            # Remember that the JavaScript client takes (and
            # gives) UTC timestamps in ms
            x = int(calendar.timegm(per.timetuple()) * 1000)
            for sg in sensor_groups:
                y = 0
                for sid in sensor_ids_by_group[sg.pk]:
                    # If this sensor has a reading for the current per,
                    # update y.  There are three ways the sensor might
                    # not have such a reading:
                    # 1. r is None, i.e. there are no more readings at
                    #    all
                    # 2. r is not None and r[2] > per, i.e. there are 
                    #    more readings but not for this per
                    # 3. r is not None and r[2] <= per and r[1] != s[0],
                    #    i.e. there are more readings for this per,
                    #    but none for this sensor
                    if r is not None and r[2] <= per and r[1] == sid:
                        # If y is None, leave it as such.   Else, add
                        # this sensor reading to y.  Afterwards, in
                        # either case, fetch a new row.
                        if y is not None:
                            y += float(r[0])
                        r = cur.fetchone()
                    else:
                        y = None
                sg_xy_pairs[sg.pk].append((x, y))
            per += per_incr
    
        d = {'no_results': False,
             'sg_xy_pairs': sg_xy_pairs,
             'show_points': max_points <= GRAPH_SHOW_POINTS_THRESHOLD,
             'sensor_groups': _get_sensor_groups()}

    json_serializer = serializers.get_serializer("json")()
    return HttpResponse(#TODO json_serializer.serialize(d, ensure_ascii=False),
                        simplejson.dumps(d),
                        mimetype='application/json')
