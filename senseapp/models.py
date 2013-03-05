from django.db import models

class Hub(models.Model):
    name     = models.CharField(max_length=255)
    address  = models.CharField(max_length=255)
    next_hop = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Thing(models.Model):
    name      = models.CharField(max_length=255)
    value     = models.IntegerField()
    hub       = models.ForeignKey(Hub)

    def __unicode__(self):
        return self.name



class Sensor(Thing):
    devices = models.ManyToManyField('Device', through='SensorDeviceRelation')

class Device(Thing):
    sensors = models.ManyToManyField('Sensor', through='SensorDeviceRelation')


class SensorDeviceRelation(models.Model):
    id       = models.AutoField(primary_key=True)
    sensor   = models.ForeignKey(Sensor)
    device   = models.ForeignKey(Device)
    relation = models.CharField(max_length=255)
