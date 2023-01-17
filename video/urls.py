from django.urls import path, re_path
from django.conf.urls import include
from .views import VideoList, VideoUpdate, VideoCreate, VideoDelete, VideoView, VideoPlayer
from .stream_views import LiveStreamList, LiveStreamUpdate, LiveStreamCreate, LiveStreamDelete, LiveStreamView, LiveStreamPlayer

urlpatterns = [

    # Video
    re_path(r'^$', VideoList.as_view(), name='video_list'),
    re_path(r'^video_list/$', VideoList.as_view(), name='video_list'),
    re_path(r'^video_add/$', VideoCreate.as_view(), name='video_add'),
    re_path(r'^video_update/(?P<pk>\w+)/$', VideoUpdate.as_view(), name='video_update'),
    re_path(r'^video_view/(?P<pk>\w+)/$', VideoView.as_view(), name='video_view'),
    re_path(r'^video_player/$', VideoPlayer.as_view(), name='player_view'),
    re_path(r'^video_delete/(?P<pk>\w+)/$', VideoDelete.as_view(), name='video_delete'),
    # LiveStream
    re_path(r'^$', LiveStreamList.as_view(), name='livestream_list'),
    re_path(r'^livestream_list/$', LiveStreamList.as_view(), name='livestream_list'),
    re_path(r'^livestream_add/$', LiveStreamCreate.as_view(), name='livestream_add'),
    re_path(r'^livestream_update/(?P<pk>\w+)/$', LiveStreamUpdate.as_view(), name='livestream_update'),
    re_path(r'^livestream_view/(?P<pk>\w+)/$', LiveStreamView.as_view(), name='livestream_view'),
    re_path(r'^livestream_player/$', LiveStreamPlayer.as_view(), name='player_view'),
    re_path(r'^livestream_delete/(?P<pk>\w+)/$', LiveStreamDelete.as_view(), name='livestream_delete'),
]
