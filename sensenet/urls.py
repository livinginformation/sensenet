from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from registration.views import register

from rest_framework.urlpatterns import format_suffix_patterns
from senseapp import views

urlpatterns = patterns('senseapp.views',
    url(r'^$', 'index', name='index'),
    url(r'^home/$', 'home', name='home'),

    url(r'^api/$', 'api_root'),
    url(r'^api/users/$', views.UserList.as_view(), name='user-list'),
    url(r'^api/users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^api/groups/$', views.GroupList.as_view(), name='group-list'),
    url(r'^api/groups/(?P<pk>\d+)/$', views.GroupDetail.as_view(), name='group-detail'),
    url(r'^api/sensors/$', views.SensorList.as_view(), name='sensor-list'),
    url(r'^api/sensors/(?P<pk>\d+)/$', views.SensorDetail.as_view(), name='sensor-detail'),
    url(r'^api/devices/$', views.DeviceList.as_view(), name='device-list'),
    url(r'^api/devices/(?P<pk>\d+)/$', views.DeviceDetail.as_view(), name='device-detail'),
    url(r'^api/hubs/$', views.HubList.as_view(), name='hub-list'),
    url(r'^api/hubs/(?P<pk>\d+)/$', views.HubDetail.as_view(), name='hub-detail'),
    url(r'^api/relations/$', views.SensorDeviceRelationList.as_view(), name='relation-list'),
    url(r'^api/relations/(?P<pk>\d+)/$', views.SensorDeviceRelationDetail.as_view(), name='relation-detail'),

    url(r'^s/$', views.SensorEvent.as_view(), name='sensor-event'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', register, {'backend': 'registration.backends.simple.SimpleBackend', 'success_url': '/' }, name='registration_register'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)