from django import forms
from django.utils.translation import ugettext as _

from baronbale_website.banner_parser.validators import validate_file_extension


class UploadGPXForm(forms.Form):
    banner_file = forms.FileField(
        label=_("GPX- or zip-File"),
        validators=[validate_file_extension.validate_file_extension],
    )
    horizontal_banners_per_row = forms.IntegerField(
        label=_("Horizontal banners per row"), min_value=1, initial=2
    )
    vertical_banners_per_row = forms.IntegerField(
        label=_("Vertical banners per row"), min_value=1, initial=3
    )
