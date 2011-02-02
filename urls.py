from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#from django.contrib import databrowse
#from graph.models import Sensor, SensorGroup, SensorReading, PowerAverage
#databrowse.site.register(Sensor)
#databrowse.site.register(SensorGroup)
#databrowse.site.register(SensorReading)
#databrowse.site.register(PowerAverage)

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/graph/'}),
    (r'^graph/', include('energyweb.graph.urls')),

    # Uncomment the following two lines so that the Django development
    # server will serve static files (js, css) for you.
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
    # {'document_root': settings.MEDIA_ROOT}),

    # Example:
    # (r'^energyweb/', include('energyweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    # (r'^databrowse/(.*)', databrowse.site.root),
)
