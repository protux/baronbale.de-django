from django.utils.translation import ugettext as _
from django import forms


class DuplicateRemoverForm(forms.Form):
    new_items = forms.CharField(
        label=_('Items to clean'),
        widget=forms.Textarea
    )

    old_items = forms.CharField(
        label=_('Already existing Items'),
        widget=forms.Textarea
    )
