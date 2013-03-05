import requests
import urllib


from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.base import TemplateView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from senseapp.serializers import *
from senseapp.models import *


#######################################################
# Index View
#######################################################

@csrf_exempt
def index(request):
    user = state = username = password = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            state = "Your username and/or password were incorrect."

    if request.user.is_authenticated():
        return redirect('home')

    return render_to_response('login.html', {'state':state, 'username': username}, RequestContext(request))

def home(request):
    if not request.user.is_authenticated():
        redirect('index')
    username = request.user.username
    sensors = Sensor.objects.all()
    devices = Device.objects.all()
    hubs = Hub.objects.all()

    return render_to_response('home.html', {'username': username, 'sensors':sensors, 'devices':devices, 'hubs':hubs}, RequestContext(request))

#######################################################
# REST api views
#
# These can be used to asynchronously perform CRUD 
# operations on the database.
#######################################################

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'groups': reverse('group-list', request=request),
        'sensors': reverse('sensor-list', request=request),
        'devices': reverse('device-list', request=request),
        'relations': reverse('relation-list', request=request),
    })

class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    model = User
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = User
    serializer_class = UserSerializer

class GroupList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Group
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Group
    serializer_class = GroupSerializer

class SensorList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    model = Sensor
    serializer_class = SensorSerializer

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Sensor
    serializer_class = SensorSerializer

class DeviceList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    model = Device
    serializer_class = DeviceSerializer

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Device
    serializer_class = DeviceSerializer

class HubList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Hub
    serializer_class = HubSerializer

class HubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Hub
    serializer_class = HubSerializer

class SensorDeviceRelationList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = SensorDeviceRelation
    serializer_class = SensorDeviceRelationSerializer

    def get_queryset(self):
        data = dict(self.request.GET.items())

        if data:
            return SensorDeviceRelation.objects.filter(sensor=data['sensor'],device=data['device'])
        else:
            return SensorDeviceRelation.objects.all()

class SensorDeviceRelationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = SensorDeviceRelation
    serializer_class = SensorDeviceRelationSerializer


#######################################################
# Event Views
#
# These are the views which are requested by the 
# arduino when an event is triggered (state change in
# a sensor). They process the event, determine which
# devices (if any) need to be updated, and then apply
# the changes.
#######################################################

class SensorEvent(View):

    def get(self, request, *args, **kwargs):

        data = dict(request.GET.items())

        sensor = Sensor.objects.get(name=data['name'])
        devices = sensor.devices.all()

        for device in devices:
            hub = device.hub
            r = requests.get("http://"+hub.address+"?*"+device.name+":"+data['val']+"@")

        return HttpResponse(r)
