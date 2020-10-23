"""video_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from django.conf.urls import url
from django.conf.urls.static import static, settings
from login import views
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


# openapi implementation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

swagger_info = openapi.Info(
        title="Video Administrator",
        default_version='latest',
        description="Administer your video on-demand and live streaming service",
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
        re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('health_check/', include('health_check.urls')),

    url(r'^$', TemplateView.as_view(template_name='static_pages/index.html'),
        name='home'),

    path('video/', include('video.urls')),
    path('login/', include('login.urls')),

    # local login
    path('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
