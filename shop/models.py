from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
import logging
from django.conf import settings
from django.contrib import messages
import json

from django.core.files.storage import FileSystemStorage
# Get an instance of a logger
logger = logging.getLogger(__name__)

fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/images/')

class ShopProvider(models.Model):
    provider = models.ForeignKey(Provider, blank=True, null=True, on_delete=models.CASCADE, help_text="Extneral or Internal Stream Host")
    name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Store")
    link = models.CharField(blank=True, null=True, max_length=255, help_text="Link to Store")
    api_key = models.CharField(blank=True, null=True, max_length=255, help_text="API key for store")
    api_password = models.CharField(blank=True, null=True, max_length=255, help_text="API Password for Auth")
    api_token = models.CharField(blank=True, null=True, max_length=255, help_text="API Token for Auth")
    store_name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Store")
    status = models.CharField(blank=True, null=True, max_length=255, help_text="Status of Provider Link")
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
        super(ShopProvider, self).save()

    def __unicode__(self):
        return self.name

class ShopProviderAdmin(admin.ModelAdmin):
    display = 'ShopProvider'
    list_display = ('name',)
    list_filter = ('name',)

# Create your models here.
class Product(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Product")
    provider = models.ForeignKey(ShopProvider, blank=True, null=True, on_delete=models.CASCADE, help_text="Extneral or Internal Stream Host")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    description = models.TextField()
    link = models.CharField(blank=True, null=True, max_length=255, help_text="Link to Product")
    token = models.CharField(blank=True, null=True, max_length=255, help_text="Auth Token")
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if self.created == None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Product, self).save()

    def __unicode__(self):
        return self.name

class ProductAdmin(admin.ModelAdmin):
    display = 'Products'
    list_display = ('name',)
    list_filter = ('name',)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.product.name


class ProductImageAdmin(admin.ModelAdmin):
    display = 'Product Images'
    list_display = ('product','image_url')
    list_filter = ('product',)
