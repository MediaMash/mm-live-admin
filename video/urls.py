from django.urls import path
from django.conf.urls import include, url
from .views import VideoList, VideoUpdate, VideoCreate, VideoDelete, VideoView, VideoPlayer
from .stream_views import LiveStreamList, LiveStreamUpdate, LiveStreamCreate, LiveStreamDelete, LiveStreamView, LiveStreamPlayer

urlpatterns = [
    # Video
    url(r'^$', VideoList.as_view(), name='video_list'),
    url(r'^video_list/$', VideoList.as_view(), name='video_list'),
    url(r'^video_add/$', VideoCreate.as_view(), name='video_add'),
    url(r'^video_update/(?P<pk>\w+)/$', VideoUpdate.as_view(), name='video_update'),
    url(r'^video_view/(?P<pk>\w+)/$', VideoView.as_view(), name='video_view'),
    url(r'^video_player/$', VideoPlayer.as_view(), name='player_view'),
    url(r'^video_delete/(?P<pk>\w+)/$', VideoDelete.as_view(), name='video_delete'),
    # LiveStream
    url(r'^$', LiveStreamList.as_view(), name='livestream_list'),
    url(r'^livestream_list/$', LiveStreamList.as_view(), name='livestream_list'),
    url(r'^livestream_add/$', LiveStreamCreate.as_view(), name='livestream_add'),
    url(r'^livestream_update/(?P<pk>\w+)/$', LiveStreamUpdate.as_view(), name='livestream_update'),
    url(r'^livestream_view/(?P<pk>\w+)/$', LiveStreamView.as_view(), name='livestream_view'),
    url(r'^livestream_player/$', LiveStreamPlayer.as_view(), name='player_view'),
    url(r'^livestream_delete/(?P<pk>\w+)/$', LiveStreamDelete.as_view(), name='livestream_delete'),
]
