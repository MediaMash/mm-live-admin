from django.contrib import admin
from .models import Video, VideoAdmin, Provider, ProviderAdmin, ProviderVideo,ProviderVideoAdmin, LiveStream, LiveStreamAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Register your models here.
admin.site.register(Video,VideoAdmin)
admin.site.register(Provider,ProviderAdmin)
admin.site.register(ProviderVideo,ProviderVideoAdmin)
admin.site.register(LiveStream,LiveStreamAdmin)
