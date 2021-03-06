"""music_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from . import views


urlpatterns = [
    #url(r'^(?P<room_id>[0-9]+)/$', views.room, name='room'),
    url(r'^(?P<room_id>[0-9]+)/(?P<client_ip>[0-9]+)/$', views.room, name='room'),
    url(r'^newroom/$', views.newroom, name='create a room'),
    url(r'^(?P<room_id>[0-9]+)/$', views.Guest_Joins_Room, name='join a room'),
    url(r'^(?P<room_id>[0-9]+)/remove/$',views.RemoveMusic, name='removeSong'),
    url(r'^user/status$', views.IdentifyUserView, name='Identify User'),
    url(r'^(?P<room_id>[0-9]+)/(?P<client_ip>[0-9]+)/addsong/$', views.add_song, name='addsong'),
    url(r'^(?P<room_id>[0-9]+)/playsong/$', views.PlaySongView, name='playsong'),
    url(r'^(?P<room_id>[0-9]+)/history/$', views.GetHistoryView, name='gethistory'),
    url(r'^(?P<room_id>[0-9]+)/queue/$', views.UpdateQueueView, name='updatequeue'),
    # url(r'^(?P<room_id>[0-9]+)/addsong/$', views.add_song, name='add a song'),
    # url(r'^(?P<room_id>[0-9]+)/playsong/$', views.play_song, name='play a song'),
]
