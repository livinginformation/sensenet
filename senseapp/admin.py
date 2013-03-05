from senseapp.models import *
from django.contrib import admin

admin.site.register(Thing)
admin.site.register(Sensor)
admin.site.register(Device)
admin.site.register(Hub)
admin.site.register(SensorDeviceRelation)