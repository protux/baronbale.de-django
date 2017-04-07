from django.utils.translation import ugettext as _
from django import forms


def get_cesar_cipher_choices(include_all):
    choices = []
    if include_all:
        choices += [(0, _('all'))]
    for idx in range(1, 26):
        choices += [(idx, idx)]
    return choices


class CesarCipherEncryptForm(forms.Form):
    plain_message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea
    )

    key = forms.ChoiceField(
        label=_('Key'),
        choices=get_cesar_cipher_choices(False),
        initial=13
    )


class CesarCipherDecryptForm(forms.Form):
    cipher_message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea
    )

    key = forms.ChoiceField(
        label=_('Key'),
        choices=get_cesar_cipher_choices(True),
        initial=0
    )


class PolybiusCipherForm(forms.Form):
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea
    )


class LetterValueCalculatorForm(forms.Form):
    options = (
        ('1', 'A=01, ..., Z=26'),
        ('2', 'A=26, ..., Z=01'),
    )

    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea
    )

    extra_values = forms.CharField(
        label=_('Extra Values'),
        widget=forms.Textarea,
        required=False
    )

    direction = forms.ChoiceField(
        label=_('Direction'),
        choices=options
    )

    offset = forms.IntegerField(
        label=_('Offset'),
        initial=0
    )

    include_numeric = forms.BooleanField(
        label=_('Include numeric values'),
        required=False
    )


class Base64EncodeFileForm(forms.Form):
    file_to_encode = forms.FileField(
        label=_('File to encode')
    )


class Base64EncodeTextForm(forms.Form):
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea
    )


class Base64DecodeForm(forms.Form):
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea
    )

    is_file = forms.BooleanField(
        label=_('Is a file'),
        required=False
    )


class UploadGPXForm(forms.Form):
    gpx_file = forms.FileField(
        label=_('GPX File')
    )
    horizontal_banners_per_row = forms.IntegerField(
        label=_('Horizontal banners per row'),
        min_value=1,
        initial=2
    )
    vertical_banners_per_row = forms.IntegerField(
        label=_('Vertical banners per row'),
        min_value=1,
        initial=3
    )
