import os
import shutil
import tempfile

from django.core.files.uploadedfile import UploadedFile


def get_temporary_directory(uploaded_file: UploadedFile) -> str:
    file_directory: str = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    _recreate_directory(file_directory)
    return file_directory


def _recreate_directory(file_directory: str) -> None:
    shutil.rmtree(file_directory, ignore_errors=True)
    os.mkdir(file_directory)
