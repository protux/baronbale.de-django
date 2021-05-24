import hashlib
import logging
import traceback
from io import BytesIO
from operator import itemgetter

import certifi
import urllib3
from PIL import Image, UnidentifiedImageError
from django.core import mail

from . import banner_parser
from baronbale_website.banner_parser.models import BannerDimension

RATIO_TAG = "ratio"
WIDTH_TAG = "width"
HEIGHT_TAG = "height"

DROP_ID = "DROP"

logger = logging.getLogger("django")


def sort_banner(banners):
    logger.info("start to sort banners")
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where(),
        timeout=urllib3.Timeout(connect=2.0, read=10.0),
    )

    for idx, banner in enumerate(banners):
        banner_url = banner[banner_parser.SRC_TAG]
        hash = hashlib.sha256(banner_url.encode("UTF-8")).hexdigest()
        banner_dimension = BannerDimension.objects.filter(banner=hash)
        if banner_dimension is not None and len(banner_dimension) > 0:
            if banner_dimension.gc_code == "":
                banner_dimension.gc_code = banner[banner_parser.GC_CODE_TAG]
                banner_dimension.url = banner_url
                banner_dimension.save()
            banner_dimension = banner_dimension[0]
            set_image_data(banner, banner_dimension)
        else:
            try:
                response = http.request(
                    "GET", normalize_url(banner[banner_parser.SRC_TAG])
                )
                if response.status == 200:
                    width, height = load_image_size(response)
                    banner_dimension = BannerDimension()
                    banner_dimension.gc_code = banner[banner_parser.GC_CODE_TAG]
                    banner_dimension.banner = hash
                    banner_dimension.url = banner_url
                    banner_dimension.ratio = width / height
                    banner_dimension.width = width
                    banner_dimension.height = height
                    banner_dimension.save()
                    set_image_data(banner, banner_dimension)
                else:
                    set_fall_back_values(banner)
            except (
                    urllib3.exceptions.NewConnectionError,
                    urllib3.exceptions.MaxRetryError,
                    UnidentifiedImageError,
            ):
                logger.info(f"Banner {banner} has no parsable image")
                banner[banner_parser.SRC_TAG] = DROP_ID
            except Exception:
                body = f"Banner: {banner}\n\nException: \n{traceback.format_exc()}"
                mail.mail_admins("Error while sorting banners", body)
                set_fall_back_values(banner)

    logger.info("sorting banner done")
    banners = [banner for banner in banners if banner[banner_parser.SRC_TAG] != DROP_ID]
    return sorted(banners, key=itemgetter(RATIO_TAG), reverse=True)


def normalize_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        if url.startswith("http:"):
            url = url.replace("http:", "http://")
        elif url.startswith("https:"):
            url = url.replace("https:", "https://")
        else:
            url = "http://" + url
    return url


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
