from django.urls import path, re_path
from django.conf.urls import include
from . import views

urlpatterns = [
    re_path(r'^login_modal$', views.login_modal),
    re_path(r'^login$', views.login_authentication),
    re_path(r'^logout$', views.logout_authentication),

]
