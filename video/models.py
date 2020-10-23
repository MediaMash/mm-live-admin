from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
import logging
from video.util import upload_video, verify_token, get_details, delete_video
from django.conf import settings
from django.contrib import messages
import json

from django.core.files.storage import FileSystemStorage
# Get an instance of a logger
logger = logging.getLogger(__name__)

fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/videos/')

PROVIDER_NAME_CHOICES = (
    ("YouTube", "YouTube"),
    ("Twitch", "Twitch"),
    ("Facebook", "Facebook"),
    ("Internal Premium", "Amazon"),
    ("Internal", "CloudFlare"),
)

class Provider(models.Model):
    name = models.CharField(choices=PROVIDER_NAME_CHOICES, blank=True, null=True, max_length=255, help_text="Name of Streaming Provider (YouTube, Twitch etc.)")
    link = models.CharField(blank=True, null=True, max_length=255, help_text="Link to Video Source")
    token = models.CharField(blank=True, null=True, max_length=255, help_text="Auth Token")
    account_key = models.CharField(blank=True, null=True, max_length=255, help_text="Account Key or ID")
    auth_email = models.CharField(blank=True, null=True, max_length=255, help_text="Authorized email of account admin")
    api_url = models.CharField(blank=True, null=True, max_length=255, help_text="API Url")
    premium = models.BooleanField(blank=True, null=True, max_length=255, help_text="Premium or Pay-Per-View Provider")
    external = models.BooleanField(blank=True, null=True, max_length=255, help_text="Extneral or Internal Provider")
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Provider"
        verbose_name_plural = "Providers"

    def save(self, *args, **kwargs):
        if self.created == None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Provider, self).save()

    def __unicode__(self):
        return self.name

class ProviderAdmin(admin.ModelAdmin):
    display = 'Providers'
    list_display = ('name',)
    list_filter = ('name',)

class ProviderVideo(models.Model):
    provider = models.ForeignKey(Provider, blank=True, null=True, on_delete=models.CASCADE, help_text="Extneral or Internal Stream Host")
    name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Video")
    link = models.CharField(blank=True, null=True, max_length=255, help_text="Link to Video Source")
    provider_id_num = models.CharField(blank=True, null=True, max_length=255, help_text="ID # From Streaming Host Provider")
    embed_code = models.CharField(blank=True, null=True, max_length=255, help_text="Code used to stream from ebeded player")
    status = models.CharField(blank=True, null=True, max_length=255, help_text="Status of Streaming Video")
    stream_id = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider ID")
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Provider Video"
        verbose_name_plural = "Provider Videos"

    def save(self, *args, **kwargs):
        if self.created == None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(ProviderVideo, self).save()

    def __unicode__(self):
        return self.name

class ProviderVideoAdmin(admin.ModelAdmin):
    display = 'ProviderVideos'
    list_display = ('name',)
    list_filter = ('name',)

class Video(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Video")
    run_time_minutes = models.CharField(blank=True, null=True, max_length=255, help_text="Length of Video Minutes")
    run_time_seconds = models.CharField(blank=True, null=True, max_length=255, help_text="Length of Video Seconds")
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, help_text="User who is the Owner of the Video")
    link = models.CharField(blank=True, null=True, max_length=255, help_text="Link to Video Source")
    direct_provider = models.ManyToManyField(ProviderVideo, blank=True, help_text="Internal Streaming Host Provider Videos", related_name="direct_provider")
    external_provider = models.ManyToManyField(ProviderVideo, blank=True, help_text="External/Social Provider Shares", related_name="external_provider")
    video_file = models.FileField(storage=fs, blank=True, null=True, max_length=255, help_text="Upload Video")
    description = models.TextField(blank=True, null=True, help_text="Description of Video")
    embed_code = models.CharField(blank=True, null=True, max_length=255, help_text="Code used to stream from ebeded player")
    status = models.CharField(blank=True, null=True, max_length=255, help_text="Status of Streaming Video")
    stream_id = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider ID")
    stream_url = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider URL")
    playback_hls = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider URL for HLS stream")
    playback_dash = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider URL for DASH stream")
    is_live = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def save(self, *args, **kwargs):
        if self.created == None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Video, self).save()
        if self.video_file is not None and self.is_live is False:
            print(self.video_file.name)
            logger.warning("Upload: " + self.video_file.name)
            logger.warning("Upload Path: " + self.video_file.path)
            stream = upload_video(file=str(self.video_file.name), path=str(self.video_file.path))
            if stream == "ERROR":
                logger.warning("Upload Failed: " + stream)
                self.is_live = False
            else:
                logger.warning("Upload SUCCESS!!: " + stream)
                self.is_live = True
                self.stream_url = str(stream)
                self.stream_id = stream.rsplit('/',1)[1]
                details = get_details(video_id=str(self.stream_id))
                print(details['result'])
                video_details=details['result']
                self.playback_hls = video_details['playback']['hls']
                self.playback_dash = video_details['playback']['dash']
                self.status = video_details['status']
        super(Video, self).save()

    def delete(self, *args, **kwargs):
        if self.video_file is not None and self.is_live is True:
            remove_stream = delete_video(video_id=str(self.stream_id))
        super(Video, self).delete()

    def __unicode__(self):
        return self.name

class VideoAdmin(admin.ModelAdmin):
    display = 'Videos'
    list_display = ('name', 'owner')
    list_filter = ('name',)


class LiveStream(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Channel")
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, help_text="User who is the Owner of the Video")
    link = models.CharField(blank=True, null=True, max_length=255, help_text="Link to Video Source")
    direct_provider = models.ManyToManyField(ProviderVideo, blank=True, help_text="Internal Streaming Host Provider Videos", related_name="stream_direct_provider")
    external_provider = models.ManyToManyField(ProviderVideo, blank=True, help_text="External/Social Provider Shares", related_name="stream_external_provider")
    live_feed_url = models.FileField(storage=fs, blank=True, null=True, max_length=255, help_text="Video Stream Feed")
    live_feed_token= models.FileField(storage=fs, blank=True, null=True, max_length=255, help_text="Video Stream Auth Token")
    description = models.TextField(blank=True, null=True, help_text="Description of Channel")
    embed_code = models.CharField(blank=True, null=True, max_length=255, help_text="Code used to stream to ebeded player")
    status = models.CharField(blank=True, null=True, max_length=255, help_text="Status of Streaming Channel")
    stream_id = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider ID")
    stream_url = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider URL")
    playback_hls = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider URL for HLS stream")
    playback_dash = models.CharField(blank=True, null=True, max_length=255, help_text="Streaming Provider URL for DASH stream")
    is_live = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "LiveStreams"
        verbose_name_plural = "LiveStreams"

    def save(self, *args, **kwargs):
        if self.created == None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(LiveStream, self).save()

    def __unicode__(self):
        return self.name

class LiveStreamAdmin(admin.ModelAdmin):
    display = 'LiveStreams'
    list_display = ('name', 'owner')
    list_filter = ('name',)
