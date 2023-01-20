from django.shortcuts import render
from django.core import serializers

import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

@method_decorator(login_required, name='dispatch')
class ProductList(ListView):
    """
    Video Report filtered by project
    """
    model = Product
    template_name = 'videos/video_list.html'

    def get(self, request, *args, **kwargs):
        get_user = User.objects.all().filter(username=request.user.username)
        get_videos = Product.objects.all()

        return render(request, self.template_name, {'getProduct': get_videos})



@method_decorator(login_required, name='dispatch')
class ProductVideoCreate(CreateView):
    """
    Using Video Form for new Video per user
    """
    model = ProductVideo
    template_name = 'videos/video_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductVideoCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProductVideoCreate, self).get_form_kwargs()
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
        messages.success(self.request, 'Success, ProductVideo Created!')
        latest = ProductVideo.objects.latest('id')
        redirect_url = '/ProductVideo/video_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProductVideoForm

@method_decorator(login_required, name='dispatch')
class ProductVideoUpdate(UpdateView):
    """
    ProductVideo Form Update an existing ProductVideo
    """
    model = ProductVideo
    template_name = 'videos/video_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductVideoUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProductVideoUpdate, self).get_form_kwargs()
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
        messages.success(self.request, 'Success, ProductVideo Updated!')
        latest = ProductVideo.objects.latest('id')
        redirect_url = '/video/video_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProductVideoForm

@method_decorator(login_required, name='dispatch')
class ProductVideoDelete(DeleteView):
    """
    ProductVideo Form Delete an existing ProductVideo
    """
    model = ProductVideo
    template_name = 'videos/video_confirm_delete.html'
    success_url = "/video/video_list"

    def dispatch(self, request, *args, **kwargs):
        return super(VideoDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Video Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = VideoForm
