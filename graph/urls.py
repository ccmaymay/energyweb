from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('graph.views',
    (r'^$', 'index'),
    (r'^(?P<data>\d+)/data.json$', 'index_data'),
    (r'^static/$', 'static_graph'),
    (r'^static/(?P<start>\d+)/to/(?P<end>\d+)/(?P<res>[a-z]+(\*10)?)/data.json$', 'static_graph_data'),
    (r'^interface/$', 'data_interface'),
)

if settings.DEBUG:
    urlpatterns += patterns('graph.views',
        (r'^(?P<data>\d+)/data.json.html$', 'index_data_html'),
        (r'^static/(?P<start>\d+)/to/(?P<end>\d+)/(?P<res>[a-z]+(\*10)?)/data.json.html$', 'static_graph_data_html'),
    )
