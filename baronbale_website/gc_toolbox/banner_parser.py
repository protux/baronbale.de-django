from django.db import transaction, IntegrityError

from .models import CacheCoordinates
from defusedxml import cElementTree
import re

GS_NAMESPACE = '{http://www.groundspeak.com/cache/1/0/1}'
TOPO_NS = '{http://www.topografix.com/GPX/1/0}'

START_TAG = 'start'
END_TAG = 'end'
GC_CODE_TAG = 'gc_code'
LATITUDE_TAG = 'latitude'
LONGITUDE_TAG = 'longitude'
TYPE_TAG = 'type'
BANNER_TAG = 'banner'
SRC_TAG = 'src'
HREF_TAG = 'href'

CACHE_URL = 'http://coords.info/{}'
BANNER_TEMPLATE = '<a href="{}">\n    <img src="{}" style="width: {}px">\n</a>\n'

BANNER_ENCODED_PATTERN = re.compile(r'&lt;a[\w\W]*?&gt;[\w\W]*?&lt;img[\w\W]*?&gt;[\w\W]*?&lt;/a&gt;', re.IGNORECASE)
BANNER_DECODED_PATTERN = re.compile(r'<a[\w\W]*?>[\w\W]*?<img[\w\W]*?>[\w\W]*?</a>', re.IGNORECASE)
IMAGE_DECODED_PATTERN = re.compile(r'<img[\w\W]*?>', re.IGNORECASE)
IMAGE_ENCODED_PATTERN = re.compile(r'&lt;img[\w\W]*?&gt;', re.IGNORECASE)
LINKLESS_IMAGE_PATTERN = re.compile(r' Banner[\w\W]*?<img.*?>', re.IGNORECASE)
SRC_PATTERN = re.compile(r'src[\w\W]*?=[\w\W]*?\"[\w\W]*?\"', re.IGNORECASE)
HREF_PATTERN = re.compile(r'href[\w\W]*?=[\w\W]*?\"[\w\W]*?\"', re.IGNORECASE)

SPECIAL_BANNERS = {
    'GC24XB5': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC24XB5',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC24XB5.jpg'
    },
    'GC2PHWJ': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2PHWJ',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2PHWJ.jpg',
    },
    'GC2PHWK': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2PHWK',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2PHWK.jpg',
    },
    'GC2KCRY': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2KCRY',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2KCRY.jpg',
    },
    'GC2PHWN': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2PHWN',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2PHWN.jpg',
    },
    'GC2PHWG': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2PHWG',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2PHWG.jpg',
    },
    'GC2PHWE': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2PHWE',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2PHWE.jpg',
    },
    'GC2PHWB': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2PHWB',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2PHWB.jpg',
    },
    'GC3REGY': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC3REGY',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC3REGY.jpg',
    },
    'GC2GJY9': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2GJY9',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2GJY9.jpg',
    },
    'GC2YMKA': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2YMKA',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2YMKA.jpg',
    },
    'GC2KCRW': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2KCRW',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2KCRW.jpg',
    },
    'GC26D16': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC26D16',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC26D16.jpg',
    },
    'GC2FX2D': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC2FX2D',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC2FX2D.jpg',
    },
    'GC3BZ1Q': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC3BZ1Q',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC3BZ1Q.jpg',
    },
    'GC47M25': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC47M25',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC47M25.jpg',
    },
    'GC511AX': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC511AX',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC511AX.jpg',
    },
    'GC537V1': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC537V1',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC537V1.jpg',
    },
    'GC5A4X9': {  # Banner on special page
        HREF_TAG: 'http://coord.info/GC5A4X9',
        SRC_TAG: 'http://wampenschleifer.de/Logos/GC5A4X9.jpg',
    },
    'GC52VPD': None,  # Zu gut für die Tonne 01 / misleading the parser (refers to banner in another cache)
    'GC52VMR': None,  # Zu gut für die Tonne 02 / misleading the parser (refers to banner in another cache)
    'GC52VNZ': None,  # Zu gut für die Tonne 03 / misleading the parser (refers to banner in another cache)
    'GC52VQA': None,  # Zu gut für die Tonne 04 / misleading the parser (refers to banner in another cache)
    'GC52VR5': None,  # Zu gut für die Tonne 05 / misleading the parser (refers to banner in another cache)
    'GC52W0J': None,  # Zu gut für die Tonne 06 / misleading the parser (refers to banner in another cache)
    'GC52W10': None,  # Zu gut für die Tonne 07 / misleading the parser (refers to banner in another cache)
    'GC52W7B': None,  # Zu gut für die Tonne 08 / misleading the parser (refers to banner in another cache)
    'GC52W7T': None,  # Zu gut für die Tonne 09 / misleading the parser (refers to banner in another cache)
    'GC52W87': None,  # Zu gut für die Tonne 10 / misleading the parser (refers to banner in another cache)
    'GC6BAZ8': None,  # Ost-West-Beziehung / misleading the parser (image refers to cache itself but is no banner)
    # Banner was deleted
    'GC4YAEY': {
        HREF_TAG: 'http://coord.info/GC4YAEY',
        SRC_TAG: 'http://imgcdn.geocaching.com/cache/large/55fcadb9-4464-483c-b43a-8152cf51f422.jpg',
    },
    'GC4432N': None,  # NighT[131]TraiN : Bonus / reference to main cache looks like a banner
}


def collect_banner_urls(path_to_xml):
    banners = dict()
    coords = []

    for event, elem in cElementTree.iterparse(path_to_xml, events=[START_TAG, END_TAG]):
        if event == START_TAG and elem.tag == '{}wpt'.format(TOPO_NS):
            latitude = elem.get('lat')
            longitude = elem.get('lon')
        elif event == END_TAG and elem.tag == '{}name'.format(TOPO_NS):
            gc_code = elem.text
        elif event == END_TAG and elem.tag == '{}url'.format(TOPO_NS):
            url = elem.text
        elif event == END_TAG and elem.tag == '{}long_description'.format(GS_NAMESPACE):
            description = elem.text
            description = strip_pattern(description, r'((alt|title)=\".*?(>|<).*?\")')
        elif event == END_TAG and elem.tag == '{}type'.format(TOPO_NS):
            type = elem.text
        elif event == END_TAG and elem.tag == '{}wpt'.format(TOPO_NS):
            try:
                if gc_code in SPECIAL_BANNERS:
                    banner = SPECIAL_BANNERS[gc_code]
                else:
                    banner = parse_banner(description, gc_code, url)

                if banner:
                    banner[HREF_TAG] = CACHE_URL.format(gc_code)
                    add_banner_to_dict(banner, banners)

                coords += [{
                    GC_CODE_TAG: gc_code,
                    LATITUDE_TAG: latitude,
                    LONGITUDE_TAG: longitude,
                    TYPE_TAG: type
                }]
            except NameError:
                pass  # too bad, provide complete gpx

    process_gc_data(coords)
    return banners.values()


def add_banner_to_dict(banner, banner_dict):
    if banner:
        banner[SRC_TAG] = banner[SRC_TAG].strip()
        src = banner[SRC_TAG]
        if src not in banner_dict:
            banner_dict[src] = banner


def get_banner_id_not_equal_to_href(banner_dict):
    if banner_dict[SRC_TAG] != banner_dict[HREF_TAG]:
        return banner_dict
    return None


def parse_banner(description, gc_code, url):
    match = BANNER_ENCODED_PATTERN.search(description)

    if match:
        banner = normalize_banner(match.group())
        return get_banner_id_not_equal_to_href(parse_banner_details(banner))

    match = IMAGE_ENCODED_PATTERN.search(description)
    if match:
        image = normalize_banner(match.group())
        src = parse_banner_details_from_image(image)
        return get_banner_id_not_equal_to_href({
            SRC_TAG: src,
            HREF_TAG: CACHE_URL.format(gc_code)
        })

    matches = BANNER_DECODED_PATTERN.finditer(description)
    for match in matches:
        banner_probe = normalize_banner(match.group())
        if contains_cache_url(banner_probe, gc_code, url):
            banner = parse_banner_details(banner_probe)
            if get_banner_id_not_equal_to_href(banner):
                return banner

    description = description.replace('bannertype', '')
    match = LINKLESS_IMAGE_PATTERN.search(description)
    if match:
        image = IMAGE_DECODED_PATTERN.search(match.group()).group()
        return get_banner_id_not_equal_to_href({
            SRC_TAG: parse_banner_details_from_image(image),
            HREF_TAG: CACHE_URL.format(gc_code)
        })

    return None


def parse_banner_details(banner):
    href = HREF_PATTERN.search(banner).group()
    href = re.sub(r'href[\w\W]*?=[\w\W]*?"', '', href).replace('"', '')
    return {
        SRC_TAG: parse_banner_details_from_image(banner),
        HREF_TAG: href,
    }


def parse_banner_details_from_image(banner):
    src = SRC_PATTERN.search(banner).group()
    src = re.sub(r'src[\w\W]*?=[\w\W]*?"', '', src)
    src = src.replace('"', '')
    return src


def process_gc_data(coord_list):
    for coord in coord_list:
        gc_code = coord[GC_CODE_TAG]
        latitude = coord[LATITUDE_TAG]
        longitude = coord[LONGITUDE_TAG]
        cache_type = coord[TYPE_TAG]

        if gc_code and latitude and longitude and gc_code != 'My Finds Pocket Query':
            cache_coordinates = CacheCoordinates()
            cache_coordinates.gc_code = gc_code
            cache_coordinates.latitude = latitude
            cache_coordinates.longitude = longitude
            try:
                if cache_type:
                    cache_type = cache_type.replace('Geocache|', '')
                    cache_coordinates.type = cache_type
            except NameError:
                cache_coordinates.type = None

            try:
                cache_coordinates.save()
            except IntegrityError:
                pass  # shut up


def normalize_banner(banner):
    banner = banner.replace('&lt;', '<')
    banner = banner.replace('&gt;', '>')
    banner = banner.replace('&amp;', '&')
    banner = banner.replace('\n', '')
    banner = banner.replace('<br />', ' ')
    banner = banner.replace('<br/>', ' ')
    banner = banner.replace('<br>', ' ')
    banner = banner.replace('</font>', '')
    banner = strip_pattern(banner, r'<font.*?>')
    banner = banner.replace('</span>', '')
    banner = strip_pattern(banner, r'<span.*?>')
    return banner


def strip_pattern(text, regex):
    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.search(text)
    while match:
        text = text.replace(match.group(0), '')
        match = pattern.search(text)
    return text


def contains_cache_url(banner_probe, gc_code, url):
    short_url = 'http://coord.info/' + gc_code
    long_url = 'geocaching.com/geocache/' + gc_code

    if short_url in banner_probe:
        return True
    if long_url in banner_probe:
        return True
    if url in banner_probe:
        return True

    return False


if __name__ == '__main__':
    from sys import argv

    if len(argv) < 2:
        print('you need to specify a path to the xml file.')
        exit(1)

    banners = collect_banner_urls(argv[1])
    for banner in banners:
        print(banner)
    print(len(banners))
