from django import forms
from django.core.validators import URLValidator
from smallurl.models import URL

class URLForm(forms.Form):
    url = forms.CharField(label='Enter a URL to shorten',
                          widget=forms.TextInput(attrs={
                              'class': 'form-control',
                              'placeholder': ''
                          }),
                          max_length=URL._meta.get_field('url').max_length)
    tls = forms.ChoiceField(label='',
                            widget=forms.Select(attrs={
                                'class': 'form-select'
                            }),
                            choices=((False, 'http'), (True, 'https')))
    custom_id = forms.CharField(label='Customise your link',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'alias'
                                }),
                                max_length=URL._meta.get_field(
                                    'id').max_length,
                                required=False)
