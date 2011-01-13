from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('graph.views',
    (r'^$', 'index'),
    (r'^(?P<data>\d+)/data.json$', 'index_data'),
    (r'^static/$', 'static_graph'),
    (r'^static/(?P<start>\d+)/to/(?P<end>\d+)/(?P<res>[a-z]+(\*10)?)/data.json$', 'static_graph_data'),
    (r'^interface/$', 'data_interface'),
)
