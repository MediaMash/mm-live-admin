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

from django.contrib.auth.models import User
from .models import Product
from .forms import ProductForm

from .util import getProducts

@method_decorator(login_required, name='dispatch')
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

@method_decorator(login_required, name='dispatch')
class ProductList(ListView):
    """
    Product Report filtered by project
    """
    model = Product
    template_name = 'shop/product_list.html'

    def get(self, request, *args, **kwargs):
        get_user = User.objects.all().filter(username=request.user.username)
        get_products = Product.objects.all()

        return render(request, self.template_name, {'getProducts': get_products})



@method_decorator(login_required, name='dispatch')
class ProductCreate(CreateView):
    """
    Using Product Form for new Product per user
    """
    model = Product
    template_name = 'shop/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProductCreate, self).get_form_kwargs()
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
        messages.success(self.request, 'Success, Product Created!')
        latest = Product.objects.latest('id')
        redirect_url = '/shop/product_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProductForm

@method_decorator(login_required, name='dispatch')
class ProductUpdate(UpdateView):
    """
    Product Form Update an existing Product
    """
    model = Product
    template_name = 'shop/Product_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProductUpdate, self).get_form_kwargs()
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
        messages.success(self.request, 'Success, Product Updated!')
        latest = Product.objects.latest('id')
        redirect_url = '/shop/product_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProductForm

@method_decorator(login_required, name='dispatch')
class ProductDelete(DeleteView):
    """
    Product Form Delete an existing Product
    """
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = "/shop/product_list"

    def dispatch(self, request, *args, **kwargs):
        return super(ProductDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Product Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProductForm


def add_provider_products(request):
    product_added = getProducts()

    if getProducts:
        return HttpResponse(json.dumps(product_added), content_type="application/json")
    else:
        message = "No Products were added, please confirm you have set up a Third Party shop provider with your Admin."
        return HttpResponse(json.dumps(message), content_type="application/json")