from django import forms
from django.utils.translation import gettext as _


class AddEmailAddressForm(forms.Form):
    email_address = forms.EmailField(label=_('Email Address'))
