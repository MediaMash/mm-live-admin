from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ShopProvider, ShopProviderAdmin)