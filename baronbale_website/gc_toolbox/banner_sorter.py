import urllib3
import certifi
import hashlib
from io import BytesIO
from operator import itemgetter
from . import banner_parser
from PIL import Image
from .models import BannerDimension

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
        hash = hashlib.sha256(banner[banner_parser.SRC_TAG].encode('UTF-8')).hexdigest()
        banner_dimension = BannerDimension.objects.filter(banner=hash)
        if banner_dimension is not None and len(banner_dimension) > 0:
            banner_dimension = banner_dimension[0]
            set_image_data(banner, banner_dimension)
        else:
            try:
                response = http.request('GET', banner[banner_parser.SRC_TAG].strip())
                if response.status == 200:
                    width, height = load_image_size(response)
                    banner_dimension = BannerDimension()
                    banner_dimension.banner = hash
                    banner_dimension.ratio = width / height
                    banner_dimension.width = width
                    banner_dimension.height = height
                    banner_dimension.save()
                    set_image_data(banner, banner_dimension)
                else:
                    set_fall_back_values(banner)
            except urllib3.exceptions.NewConnectionError:
                set_fall_back_values(banner)
            except urllib3.exceptions.MaxRetryError:
                set_fall_back_values(banner)
            except OSError:
                set_fall_back_values(banner)

    return sorted(banners, key=itemgetter(RATIO_TAG), reverse=True)


def load_image_size(response):
    image = Image.open(BytesIO(response.data))
    return image.size


def set_image_data(banner, banner_dimension):
    banner[RATIO_TAG] = banner_dimension.ratio
    banner[WIDTH_TAG] = banner_dimension.width
    banner[HEIGHT_TAG] = banner_dimension.height


def set_fall_back_values(banner):
    banner[RATIO_TAG] = 0.0
    banner[WIDTH_TAG] = 0
    banner[HEIGHT_TAG] = 0
