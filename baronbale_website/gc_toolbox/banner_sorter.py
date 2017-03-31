import urllib3
import certifi
from io import BytesIO
from operator import itemgetter
from . import banner_parser
from PIL import Image

RATIO_TAG = 'ratio'
WIDTH_TAG = 'width'
HEIGHT_TAG = 'height'


def sort_banner(banners):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where(),
        timeout=urllib3.Timeout(connect=2.0, read=10.0)
    )

    for banner in banners:
        try:
            response = http.request('GET', banner[banner_parser.SRC_TAG])
            if response.status == 200:
                set_image_data(banner, response)
            else:
                set_fall_back_values(banner)
        except urllib3.exceptions.NewConnectionError:
            set_fall_back_values(banner)
        except urllib3.exceptions.MaxRetryError:
            set_fall_back_values(banner)

    return sorted(banners, key=itemgetter(RATIO_TAG), reverse=True)


def set_image_data(banner, response):
    image = Image.open(BytesIO(response.data))
    width, height = image.size
    banner[RATIO_TAG] = width / height
    banner[WIDTH_TAG] = width
    banner[HEIGHT_TAG] = height


def set_fall_back_values(banner):
    banner[RATIO_TAG] = 0.0
    banner[WIDTH_TAG] = 0
    banner[HEIGHT_TAG] = 0
