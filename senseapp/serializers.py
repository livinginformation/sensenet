from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from senseapp.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.ManySlugRelatedField(
        slug_field='codename',
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions')

class SensorSerializer(serializers.ModelSerializer):
    id = serializers.Field()

    class Meta:
        model = Sensor
        fields = ('id','name', 'value', 'hub', 'devices')

class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.Field()

    class Meta:
        model = Device
        fields = ('id','name', 'value', 'hub', 'sensors')

class HubSerializer(serializers.ModelSerializer):
    id = serializers.Field()

    class Meta:
        model = Hub
        fields = ('id', 'name', 'address', 'next_hop', 'value', 'sensor_set')

class SensorDeviceRelationSerializer(serializers.ModelSerializer):
    id = serializers.Field()

    class Meta:
        model = SensorDeviceRelation
        fields = ('id', 'sensor', 'device', 'relation')