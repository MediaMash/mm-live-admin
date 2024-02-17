from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from .views import VideoList, VideoUpdate, VideoCreate, VideoDelete, VideoView, VideoPlayer, VideoPlayer2, publish_youtube, publish_vimeo, VideoViewSet, ProductViewSet, VideoProductViewSet
from .stream_views import LiveStreamList, LiveStreamUpdate, LiveStreamCreate, LiveStreamDelete, LiveStreamView, LiveStreamPlayer
from . import stream_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'videoproduct', VideoProductViewSet, basename='videoproduct')


urlpatterns = [

    #rest service
    path('api/', include(router.urls)),

    # Video
    re_path(r'^$', VideoList.as_view(), name='video_list'),
    re_path(r'^video_list/$', VideoList.as_view(), name='video_list'),
    re_path(r'^video_add/$', VideoCreate.as_view(), name='video_add'),
    re_path(r'^video_update/(?P<pk>\w+)/$', VideoUpdate.as_view(), name='video_update'),
    re_path(r'^video_view/(?P<pk>\w+)/$', VideoView.as_view(), name='video_view'),
    re_path(r'^video_player/$', VideoPlayer.as_view(), name='player_view'),
    re_path(r'^video_player2/$', VideoPlayer2.as_view(), name='player_view2'),
    re_path(r'^video_delete/(?P<pk>\w+)/$', VideoDelete.as_view(), name='video_delete'),
    re_path(r'^publish_youtube/(?P<pk>\w+)/$', publish_youtube, name='publish_youtube'),
    re_path(r'^publish_vimeo/(?P<pk>\w+)/$', publish_vimeo, name='publish_vimeo'),
    # platform stream
    url(r'^go_live/$', stream_views.go_live, name='go_live'),
    # LiveStream
    re_path(r'^$', LiveStreamList.as_view(), name='livestream_list'),
    re_path(r'^livestream_list/$', LiveStreamList.as_view(), name='livestream_list'),
    re_path(r'^livestream_add/$', LiveStreamCreate.as_view(), name='livestream_add'),
    re_path(r'^livestream_update/(?P<pk>\w+)/$', LiveStreamUpdate.as_view(), name='livestream_update'),
    re_path(r'^livestream_view/(?P<pk>\w+)/$', LiveStreamView.as_view(), name='livestream_view'),
    re_path(r'^livestream_player/$', LiveStreamPlayer.as_view(), name='player_view'),
    re_path(r'^livestream_delete/(?P<pk>\w+)/$', LiveStreamDelete.as_view(), name='livestream_delete'),

]
