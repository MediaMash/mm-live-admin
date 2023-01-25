import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field, LayoutObject, TEMPLATE_PACK

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Product



class ProductForm(forms.ModelForm):
    """
    Form for uploading a new product.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'link','upc_code']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(ProductForm, self).__init__(*args, **kwargs)

    helper = FormHelper()
    helper.form_class = 'form-vertical'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'
    helper.form_error_title = 'Form Errors'
    helper.error_text_inline = True
    helper.help_text_inline = True
    helper.html5_required = True
    helper.layout = Layout(
        HTML("""<br/>"""),
        TabHolder(
            Tab('Product Details',
             Fieldset('',
                'name', 'description', 'link','upc_code'
                ),
            ),
        ),

        HTML("""<br/>"""),

        Submit('submit', 'Submit', css_class='btn-default'),
        Reset('reset', 'Reset', css_class='btn-warning'))

