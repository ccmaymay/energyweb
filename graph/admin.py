from graph.models import Sensor, SensorGroup, SensorReading, PowerAverage
from django.contrib import admin

admin.site.register(SensorGroup)
admin.site.register(Sensor)
admin.site.register(SensorReading)
admin.site.register(PowerAverage)
