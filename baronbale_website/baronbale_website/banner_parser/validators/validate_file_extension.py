from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.translation import gettext as _


def validate_file_extension(uploaded_file: TemporaryUploadedFile) -> None:
    file_name = uploaded_file.name
    if not file_name.endswith(".gpx") and not file_name.endswith(".zip"):
        raise ValidationError(_("You need to provide either a *.gpx or a *.zip file."))
