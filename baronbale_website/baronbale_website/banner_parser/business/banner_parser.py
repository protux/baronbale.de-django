import logging
import multiprocessing
import re
import traceback

from defusedxml import cElementTree
from django.core import mail

from baronbale_website.banner_parser.business import killable_banner_parser
from baronbale_website.banner_parser.models import BannerCache

logger = logging.getLogger("django")

GS_NAMESPACE_OLD = "{http://www.groundspeak.com/cache/1/0/1}"
GS_NAMESPACE_NEW = "{http://www.groundspeak.com/cache/1/0}"
TOPO_NS = "{http://www.topografix.com/GPX/1/0}"

START_TAG = "start"
END_TAG = "end"
GC_CODE_TAG = "gc_code"
LATITUDE_TAG = "latitude"
LONGITUDE_TAG = "longitude"
TYPE_TAG = "type"
BANNER_TAG = "banner"
SRC_TAG = "src"
HREF_TAG = "href"

CACHE_URL = "https://coord.info/{}"
BANNER_TEMPLATE = '<a href="{}">\n    <img src="{}" style="width: {}%">\n</a>\n'

BANNER_ENCODED_PATTERN = re.compile(
    r"&lt;a[\w\W]*?&gt;[\w\W]*?&lt;img[\w\W]*?&gt;[\w\W]*?&lt;/a&gt;", re.IGNORECASE
)
BANNER_DECODED_PATTERN = re.compile(
    r"<a[\w\W]*?>[\w\W]*?<img[\w\W]*?>[\w\W]*?</a>", re.IGNORECASE
)
IMAGE_DECODED_PATTERN = re.compile(r"<img[\w\W]*?>", re.IGNORECASE)
IMAGE_ENCODED_PATTERN = re.compile(r"&lt;img[\w\W]*?&gt;", re.IGNORECASE)
LINKLESS_IMAGE_PATTERN = re.compile(r" Banner[\w\W]*?<img.*?>", re.IGNORECASE)
SRC_PATTERN = re.compile(r"src[\w\W]*?=[\w\W]*?[\"\'][\w\W]*?[\"\']", re.IGNORECASE)
HREF_PATTERN = re.compile(r"href[\w\W]*?=[\w\W]*?[\"\'][\w\W]*?[\"\']", re.IGNORECASE)


def collect_banner_urls(gpx_files):
    logger.info("Start collecting Banner information...")
    banners = dict()
    special_banners = special_banners_to_dict()

    for path_to_xml in gpx_files:
        for event, elem in cElementTree.iterparse(
                path_to_xml, events=[START_TAG, END_TAG]
        ):
            if event == END_TAG and elem.tag == "{}name".format(TOPO_NS):
                gc_code = elem.text
            elif event == END_TAG and elem.tag == "{}url".format(TOPO_NS):
                url = elem.text
            elif event == END_TAG and elem.tag == "{}long_description".format(
                    GS_NAMESPACE_OLD
            ):
                description = elem.text
                description = killable_banner_parser.strip_pattern(
                    description, r"((alt|title)=\".*?(>|<).*?\")"
                )
            elif event == END_TAG and elem.tag == "{}long_description".format(
                    GS_NAMESPACE_NEW
            ):
                description = elem.text
                description = killable_banner_parser.strip_pattern(
                    description, r"((alt|title)=\".*?(>|<).*?\")"
                )
            elif event == END_TAG and elem.tag == "{}wpt".format(TOPO_NS):
                try:
                    if gc_code in special_banners:
                        logger.info(f"Served {gc_code} from cache.")
                        banner = special_banners[gc_code]
                    else:
                        try:
                            logger.info(f"Investigating {gc_code}...")
                            banner = _parse_banners(description, gc_code, url)
                        except Exception:
                            logger.exception("Error while parsing banner")
                            body = f"exception: \n{traceback.format_exc()}"
                            mail.mail_admins("Error while parsing banner", body)

                    if banner:
                        banner[HREF_TAG] = CACHE_URL.format(gc_code)
                        add_banner_to_dict(banner, banners)
                except NameError:
                    logger.info(
                        "It seems a GPX-file was incomplete. "
                        "Some caches could not be read."
                    )
    logger.info("...finished collecting Banner information")
    return banners.values()


def _parse_banners(description, gc_code, url):
    banner = dict()
    process = multiprocessing.Process(
        target=killable_banner_parser.parse_banner,
        args=(description, gc_code, url, banner),
    )
    process.start()
    process.join(15)
    if process.is_alive():
        logger.warning(f"Parsing took too long, killing parser for {gc_code}")
        process.kill()
        process.join(1)
    return banner


def special_banners_to_dict():
    special_banners = {}
    for special_banner in BannerCache.objects.all():
        if special_banner.image_url is None:
            special_banners.update({special_banner.gc_code: None})
        else:
            special_banners.update(
                {
                    special_banner.gc_code: {
                        HREF_TAG: CACHE_URL.format(special_banner.gc_code),
                        SRC_TAG: special_banner.image_url,
                    }
                }
            )
    return special_banners


def add_banner_to_dict(banner, banner_dict):
    if banner:
        banner[SRC_TAG] = banner[SRC_TAG].strip()
        src = banner[SRC_TAG]
        if src not in banner_dict:
            banner_dict[src] = banner
