import datetime
import logging
import os
import shutil
import tempfile
import zipfile

from django.conf import settings
from django.utils.translation import ugettext as _

from baronbale_website.gc_toolbox import banner_sorter, banner_parser
from baronbale_website.gc_toolbox import exceptions
from baronbale_website.gc_toolbox.tools import exceptions as tool_exceptions

BANNERTOOL_SUBDIRECTORY = os.path.join(settings.MEDIA_ROOT, "bannertool")
UPLOADED_FILES_SUBDIRECTORY = os.path.join(BANNERTOOL_SUBDIRECTORY, "uploads")

MARGIN_BETWEEN_BANNER = 0.5

logger = logging.getLogger("django")


def build_destination_filename(input_file, now=datetime.datetime.utcnow()):
    timestamp_string = now.strftime("%Y%m%d_%H%M%S")
    if "." in input_file:
        file_ending = input_file.split(".")[-1]
        file_name = timestamp_string + "." + file_ending
    else:
        file_name = timestamp_string
    return file_name


def backup_file_gpx_to_media(input_file):
    os.makedirs(UPLOADED_FILES_SUBDIRECTORY, exist_ok=True)
    file_name = build_destination_filename(input_file)
    destination_file = os.path.join(UPLOADED_FILES_SUBDIRECTORY, file_name)
    shutil.copyfile(input_file, destination_file)


def backup_file_to_media(uploaded_file):
    os.makedirs(UPLOADED_FILES_SUBDIRECTORY, exist_ok=True)
    file_name = build_destination_filename(uploaded_file.name)
    destination_file = os.path.join(UPLOADED_FILES_SUBDIRECTORY, file_name)
    write_uploaded_file(destination_file, uploaded_file)
    return destination_file


def strip_non_gpx_files_from_zip(file_list: []):
    filtered_list = []
    for file in file_list:
        if file.endswith(".gpx"):
            filtered_list += [file]
    return filtered_list


def extract_gpx_if_needed(uploaded_file):
    temp_directory = get_temporary_directory(uploaded_file)

    file_path = backup_file_to_media(uploaded_file)
    if uploaded_file.name.endswith(".zip"):
        output_files = extract_zip(temp_directory, file_path)
    elif uploaded_file.name.endswith(".gpx"):
        output_files = [file_path]
    else:
        raise exceptions.InvalidFileException(
            _("You uploaded a not supported file type.")
        )

    return output_files


def write_uploaded_file(input_file, uploaded_file):
    with open(input_file, "wb") as output:
        output.write(uploaded_file.read())
    return [input_file]


def extract_zip(temp_directory, uploaded_file):
    with zipfile.ZipFile(uploaded_file, "r") as zip_file:
        contained_files = zip_file.namelist()
        gpx_files = strip_non_gpx_files_from_zip(contained_files)
        if len(gpx_files) == 0:
            raise tool_exceptions.EmptyZipException()
        zip_file.extractall(path=temp_directory, members=gpx_files)
        extracted_files = []
        for listed_file in os.listdir(temp_directory):
            extracted_files += [os.path.join(temp_directory, listed_file)]
        return extracted_files


def get_temporary_directory(uploaded_file):
    file_directory = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    recreate_directory(file_directory)
    return file_directory


def recreate_directory(file_directory):
    try:
        os.mkdir(file_directory)
    except FileExistsError:
        shutil.rmtree(file_directory, ignore_errors=True)
        os.mkdir(file_directory)


def join_banners(banners, horizontal_banners_per_row, vertical_banners_per_row):
    joined_banners = ""
    balanced_output = False

    for idx, banner in enumerate(banners):
        if banner[banner_sorter.RATIO_TAG] > 1.0:  # if horizontal
            joined_banners += (
                get_formatted_banner(banner, horizontal_banners_per_row) + "\n"
            )
        elif (
            not balanced_output
            and idx % horizontal_banners_per_row > 0
            and banner[banner_sorter.RATIO_TAG] <= 1.0
        ):
            joined_banners += (
                get_formatted_banner(banner, horizontal_banners_per_row) + "\n"
            )
            if idx % horizontal_banners_per_row == horizontal_banners_per_row - 1:
                balanced_output = True
        else:
            joined_banners += (
                get_formatted_banner(banner, vertical_banners_per_row) + "\n"
            )
            balanced_output = True

    return joined_banners + "\n"


def get_formatted_banner(banner, banner_per_row):
    return banner_parser.BANNER_TEMPLATE.format(
        banner[banner_parser.HREF_TAG],
        banner[banner_parser.SRC_TAG],
        calculate_banner_width(banner_per_row),
    )


def calculate_banner_width(banners_per_row):
    return round(100 / banners_per_row - MARGIN_BETWEEN_BANNER, 2)
