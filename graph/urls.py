from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('energyweb.graph.views',
    (r'^$', 'dynamic_graph'),
    (r'^(?P<data>\d+)/data.json$', 'dynamic_graph_data'),
    (r'^static/$', 'static_graph'),
    (r'^static/(?P<start>\d+)/to/(?P<end>\d+)/(?P<res>[a-z]+(\*10)?)/data.json$', 'static_graph_data'),
    (r'^interface/$', 'data_interface'),
)

if settings.DEBUG:
    # Add views for HTML-wrappings of the JSON data views.
    urlpatterns += patterns('energyweb.graph.views',
        (r'^(?P<data>\d+)/data.json.html$', 'dynamic_graph_data_html'),
        (r'^static/(?P<start>\d+)/to/(?P<end>\d+)/(?P<res>[a-z]+(\*10)?)/data.json.html$', 'static_graph_data_html'),
    )
