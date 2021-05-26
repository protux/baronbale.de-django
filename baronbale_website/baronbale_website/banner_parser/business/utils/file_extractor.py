import zipfile
from typing import List
import os

from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext as _

from baronbale_website.banner_parser.business.utils import (
    directory_provider,
    file_storage,
)
from baronbale_website.banner_parser.business.utils.exceptions import (
    EmptyZipException,
    InvalidFileException,
)


def extract_gpx_if_needed(uploaded_file: UploadedFile) -> List[str]:
    temp_directory: str = directory_provider.get_temporary_directory(uploaded_file)

    file_path: str = file_storage.backup_file_to_media(uploaded_file)
    if uploaded_file.name.endswith(".zip"):
        output_files: List[str] = _extract_zip(temp_directory, file_path)
    elif uploaded_file.name.endswith(".gpx"):
        output_files: List[str] = [file_path]
    else:
        raise InvalidFileException(_("You uploaded a not supported file type."))

    return output_files


def _extract_zip(temp_directory: str, file_name: str) -> List[str]:
    with zipfile.ZipFile(file_name, "r") as zip_file:
        contained_files: List = zip_file.namelist()
        gpx_files = _strip_non_gpx_files_from_zip(contained_files)
        if len(gpx_files) == 0:
            raise EmptyZipException()
        zip_file.extractall(path=temp_directory, members=gpx_files)
        extracted_files: List[str] = [
            os.path.join(temp_directory, listed_file)
            for listed_file in os.listdir(temp_directory)
        ]
        return extracted_files


def _strip_non_gpx_files_from_zip(file_list: List[str]) -> List[str]:
    filtered_list: List[str] = [file for file in file_list if file.endswith(".gpx")]
    return filtered_list
