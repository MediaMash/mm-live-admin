import json
import warnings
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic.list import ListView
from .models import LiveStream
from .forms import LiveStreamForm
from .util import get_details

from django.contrib.auth.models import User

@method_decorator(login_required, name='dispatch')
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


@method_decorator(login_required, name='dispatch')
class LiveStreamList(ListView):
    """
    LiveStream Report filtered by project
    """
    model = LiveStream
    template_name = 'livestreams/livestream_list.html'

    def get(self, request, *args, **kwargs):
        get_user = User.objects.all().filter(username=request.user.username)
        get_livestreams = LiveStream.objects.all()

        return render(request, self.template_name, {'getLiveStreams': get_livestreams})


@method_decorator(login_required, name='dispatch')
class LiveStreamView(View):
    """
    LiveStream Detail View
    """
    model = LiveStream
    template_name = 'livestreams/view_livestream.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        get_livestream = LiveStream.objects.get(pk=id)
        details = get_details(get_livestream.stream_id)
        return render(request, self.template_name, {'getLiveStream': get_livestream, 'getDetails': details})



@method_decorator(login_required, name='dispatch')
class LiveStreamPlayer(View):
    """
    LiveStream Detail View
    """
    model = LiveStream
    template_name = 'player_example.html'

    def get(self, request, *args, **kwargs):
        get_livestreams = LiveStream.objects.all()
        return render(request, self.template_name, {'getLiveStreams': get_livestreams})

@method_decorator(login_required, name='dispatch')
class LiveStreamCreate(CreateView):
    """
    Using LiveStream Form for new LiveStream per user
    """
    model = LiveStream
    template_name = 'livestreams/livestream_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(LiveStreamCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(LiveStreamCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):

        initial = {
            'user': self.request.user,
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, LiveStream Created!')
        latest = LiveStream.objects.latest('id')
        redirect_url = '/video/livestream_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = LiveStreamForm

@method_decorator(login_required, name='dispatch')
class LiveStreamUpdate(UpdateView):
    """
    LiveStream Form Update an existing livestream
    """
    model = LiveStream
    template_name = 'livestreams/livestream_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(LiveStreamUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(LiveStreamUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):

        initial = {
            'user': self.request.user,
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, LiveStream Updated!')
        latest = LiveStream.objects.latest('id')
        redirect_url = '/video/livestream_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = LiveStreamForm

@method_decorator(login_required, name='dispatch')
class LiveStreamDelete(DeleteView):
    """
    LiveStream Form Delete an existing LiveStream
    """
    model = LiveStream
    template_name = 'video/livestream_confirm_delete.html'
    success_url = "/video/livestream_list"

    def dispatch(self, request, *args, **kwargs):
        return super(LiveStreamDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, LiveStream Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = LiveStreamForm


def logout_view(request):
    """
    Logout a user in activity and track
    """
    # Redirect to track, so the user will
    # be logged out there as well
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("/")

    return HttpResponseRedirect("/")


def check_view(request):
    return HttpResponse("Hostname "+request.get_host())


from django.shortcuts import render, redirect
from ffmpeg import FFmpeg

def go_live(request):
    # Get the streaming platform, i.e. YouTube or Twitch
    platform = request.POST.get('platform')
    # Get the HLS stream URL
    hls_stream = request.POST.get('hls_stream')
    try:
        ff = FFmpeg(inputs={hls_stream: None}, outputs={
            f'rtmp://a.rtmp.youtube.com/live2/{YOUR_YOUTUBE_STREAM_KEY}': None,
            f'rtmp://live-{YOUR_TWITCH_REGION}.twitch.tv/app/{YOUR_TWITCH_STREAM_KEY}': None
        })
        # Start the stream
        ff.run()
    except Exception as e:
        print(f'An error occurred: {e}')
        return render(request, 'error.html')
    if platform == 'youtube':
        return redirect(f'https://www.youtube.com/watch?v={YOUR_YOUTUBE_STREAM_KEY}')
    elif platform == 'twitch':
        return redirect(f'https://www.twitch.tv/{YOUR_TWITCH_USERNAME}')
    else:
        return render(request, '500.html', {'error': 'Invalid platform'})

