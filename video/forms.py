import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field, LayoutObject, TEMPLATE_PACK

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Video, LiveStream


class RegistrationForm(UserChangeForm):
    """
    Form for registering a new account.
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = '__all__'

    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'
    helper.form_error_title = 'Form Errors'
    helper.error_text_inline = True
    helper.help_text_inline = True
    helper.html5_required = True
    helper.layout = Layout(
                           Submit('submit', 'Submit', css_class='btn-default'),
                           Reset('reset', 'Reset', css_class='btn-warning'))


class NewUserRegistrationForm(UserCreationForm):
    """
    Form for registering a new account.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super(NewUserRegistrationForm, self).__init__(*args, **kwargs)

    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'
    helper.form_error_title = 'Form Errors'
    helper.error_text_inline = True
    helper.help_text_inline = True
    helper.html5_required = True
    helper.form_tag = False


class VideoForm(forms.ModelForm):
    """
    Form for uploading a new video.
    """
    class Meta:
        model = Video
        fields = ['name', 'description', 'owner', 'link', 'video_file','run_time_minutes',
        'run_time_seconds', 'direct_provider','external_provider','is_live', 'related_products']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(VideoForm, self).__init__(*args, **kwargs)

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
            Tab('Video Details',
             Fieldset('',
                'name', 'description', 'owner', 'video_file',Field('is_live', disabled=True),'related_products',
                ),
            ),
        ),
        HTML("""<br/>"""),
        FormActions(
            Submit('submit', 'Save', css_class='btn-default'),
            Reset('reset', 'Reset', css_class='btn-warning')
        )
    )


class LiveStreamForm(forms.ModelForm):
    """
    Form for uploading a new LiveStream.
    """
    class Meta:
        model = LiveStream
        fields = ['name', 'description', 'owner', 'link', 'live_feed_url','live_feed_token'
        ,'embed_code','direct_provider','external_provider','is_live']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(LiveStreamForm, self).__init__(*args, **kwargs)

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
            Tab('Video Details',
             Fieldset('',
                'name', 'description', 'owner', 'live_feed_url','live_feed_token'
                'embed_code',Field('is_live', disabled=True),
                ),
            ),
        ),

        HTML("""<br/>"""),
        FormActions(
            Submit('submit', 'Save', css_class='btn-default'),
            Reset('reset', 'Reset', css_class='btn-warning')
        )
    )