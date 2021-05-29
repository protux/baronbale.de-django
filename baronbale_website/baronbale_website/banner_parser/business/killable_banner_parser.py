import re

from bs4 import BeautifulSoup

CACHE_URL = "https://coord.info/{}"
BANNER_TEMPLATE = '<a href="{}">\n    <img src="{}" style="width: {}%">\n</a>\n'

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


def parse_banner(description, gc_code, url, banner_return_dict: dict):
    description = description.replace("SRC=", "src=")
    match = BANNER_ENCODED_PATTERN.search(description)

    if match:
        banner = normalize_banner(match.group())
        banner_return_dict.update(
            get_banner_id_not_equal_to_href(parse_banner_details(banner))
        )

    soup = BeautifulSoup(description, "lxml")
    links = soup.find_all("a")
    if links:
        for link in links:
            image = link.find("img")
            if (
                    image is not None
                    and image.get("src", None)
                    and link.get("href", None)
                    and contains_cache_url(link.get("href"), gc_code, url)
            ):
                banner_return_dict.update(
                    get_banner_id_not_equal_to_href(
                        {SRC_TAG: image["src"], HREF_TAG: CACHE_URL.format(gc_code)}
                    )
                )

    matches = BANNER_DECODED_PATTERN.finditer(description)
    for match in matches:
        banner_probe = normalize_banner(match.group())
        if contains_cache_url(banner_probe, gc_code, url):
            banner = parse_banner_details(banner_probe)
            if get_banner_id_not_equal_to_href(banner):
                banner_return_dict.update(banner)

    description = description.replace("bannertype", "")
    match = LINKLESS_IMAGE_PATTERN.search(description)
    if match:
        image = IMAGE_DECODED_PATTERN.search(match.group()).group()
        banner_return_dict.update(
            get_banner_id_not_equal_to_href(
                {
                    SRC_TAG: parse_banner_details_from_image(image),
                    HREF_TAG: CACHE_URL.format(gc_code),
                }
            )
        )

    return None


def normalize_banner(banner):
    banner = banner.replace("&lt;", "<")
    banner = banner.replace("&gt;", ">")
    banner = banner.replace("&amp;", "&")
    banner = banner.replace("\n", "")
    banner = banner.replace("<br />", " ")
    banner = banner.replace("<br/>", " ")
    banner = banner.replace("<br>", " ")
    banner = banner.replace("</font>", "")
    banner = strip_pattern(banner, r"<font.*?>")
    banner = banner.replace("</span>", "")
    banner = strip_pattern(banner, r"<span.*?>")
    return banner


def get_banner_id_not_equal_to_href(banner_dict):
    if banner_dict[SRC_TAG] != banner_dict[HREF_TAG]:
        return banner_dict
    return None


def parse_banner_details(banner):
    href = HREF_PATTERN.search(banner).group()
    href = (
        re.sub(r'href[\w\W]*?=[\w\W]*?["\']', "", href)
            .replace('"', "")
            .replace("'", "")
    )
    return {
        SRC_TAG: parse_banner_details_from_image(banner),
        HREF_TAG: href,
    }


def contains_cache_url(banner_probe, gc_code, url):
    short_url = "http://coord.info/" + gc_code
    long_url = "geocaching.com/geocache/" + gc_code

    if banner_probe is not None:
        if short_url in banner_probe:
            return True
        if long_url in banner_probe:
            return True
        if url in banner_probe:
            return True

    return False


def parse_banner_details_from_image(banner):
    src = SRC_PATTERN.search(banner).group()
    src = re.sub(r'src[\w\W]*?=[\w\W]*?["\']', "", src)
    src = src.replace('"', "").replace("'", "").replace("<a>", "").replace("</a>", "")
    src = re.sub(r"\s+", "", src)
    return src


def strip_pattern(text, regex):
    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.search(text)
    while match:
        text = text.replace(match.group(0), "")
        match = pattern.search(text)
    return text
