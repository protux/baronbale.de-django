import os
from datetime import datetime

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

BANNER_TOOL_SUBDIRECTORY = os.path.join(settings.MEDIA_ROOT, "bannertool")
UPLOADED_FILES_SUBDIRECTORY = os.path.join(BANNER_TOOL_SUBDIRECTORY, "uploads")


def backup_file_to_media(uploaded_file: UploadedFile) -> str:
    os.makedirs(UPLOADED_FILES_SUBDIRECTORY, exist_ok=True)
    file_name: str = _build_destination_filename(uploaded_file.name)
    destination_file: str = os.path.join(UPLOADED_FILES_SUBDIRECTORY, file_name)
    _write_uploaded_file(destination_file, uploaded_file)
    return destination_file


def _build_destination_filename(input_file: str, now=datetime.utcnow()) -> str:
    timestamp_string: str = now.strftime("%Y%m%d_%H%M%S")
    if "." in input_file:
        file_ending: str = input_file.split(".")[-1]
        file_name: str = timestamp_string + "." + file_ending
    else:
        file_name: str = timestamp_string
    return file_name


def _write_uploaded_file(input_file: str, uploaded_file: UploadedFile) -> None:
    with open(input_file, "wb") as output:
        output.write(uploaded_file.read())
