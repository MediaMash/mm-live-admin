from django.urls import path, re_path
from django.conf.urls import url
from django.conf.urls import include
from .views import ProductList, ProductUpdate, ProductCreate, ProductDelete, add_provider_products

urlpatterns = [

    # Product
    re_path(r'^$', ProductList.as_view(), name='product_list'),
    re_path(r'^product_list/$', ProductList.as_view(), name='product_list'),
    re_path(r'^product_add/$', ProductCreate.as_view(), name='product_add'),
    re_path(r'^product_update/(?P<pk>\w+)/$', ProductUpdate.as_view(), name='product_update'),
    re_path(r'^product_delete/(?P<pk>\w+)/$', ProductDelete.as_view(), name='product_delete'),
    re_path(r'^get_products/$', add_provider_products, name='get_products'),

]
