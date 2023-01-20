from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Product")
    description = models.CharField(blank=True, null=True, max_length=255, help_text="Name of Product")
    upc_code = models.CharField(blank=True, null=True, max_length=255, help_text="Unique Product Code")
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