from .models import CacheCoordinates
from defusedxml import cElementTree
import re

GS_NAMESPACE = '{http://www.groundspeak.com/cache/1/0/1}'
TOPO_NS = '{http://www.topografix.com/GPX/1/0}'

START_TAG = 'start'
END_TAG = 'end'

BANNER_ENCODED_PATTERN = re.compile(r'&lt;a.*?&gt;.*?&lt;img.*?&gt;.*?&lt;/a&gt;', re.IGNORECASE)
BANNER_DECODED_PATTERN = re.compile(r'<a.*?>.*?<img.*?>.*?</a>', re.IGNORECASE)
IMAGE_DECODED_PATTERN = re.compile(r'<img.*?>', re.IGNORECASE)
IMAGE_ENCODED_PATTERN = re.compile(r'&lt;img.*?&gt;', re.IGNORECASE)
LINKLESS_IMAGE_PATTERN = re.compile(r' Banner[\w\W]*?<img.*?>', re.IGNORECASE)
SRC_PATTERN = re.compile(r'src.*?=.*?\".*?\"', re.IGNORECASE)

SPECIAL_BANNERS = {
    'GC24XB5': '<a href="http://coord.info/GC24XB5"><img src="http://wampenschleifer.de/Logos/GC24XB5.jpg" alt="GC24XB5 - Arbeitsschutzbeauftragter Obmann"></a>',  # Banner on special page
    'GC2PHWJ': '<a href="http://coord.info/GC2PHWJ"><img src="http://wampenschleifer.de/Logos/GC2PHWJ.jpg" alt="GC2PHWJ - Der Bibliothekar"></a>',  # Banner on special page
    'GC2PHWK': '<a href="http://coord.info/GC2PHWK"><img src="http://wampenschleifer.de/Logos/GC2PHWK.jpg" alt="GC2PHWK - Der Elektriker"></a>',  # Banner on special page
    'GC2KCRY': '<a href="http://coord.info/GC2KCRY"><img src="http://wampenschleifer.de/Logos/GC2KCRY.jpg" alt="GC2KCRY - Der Fabrikarbeiter"></a>',  # Banner on special page
    'GC2PHWN': '<a href="http://coord.info/GC2PHWN"><img src="http://wampenschleifer.de/Logos/GC2PHWN.jpg" alt="GC2PHWN - Der Geschichtstudent"></a>',  # Banner on special page
    'GC2PHWG': '<a href="http://coord.info/GC2PHWG"><img src="http://wampenschleifer.de/Logos/GC2PHWG.jpg" alt="GC2PHWG - Der Manager"></a>',  # Banner on special page
    'GC2PHWE': '<a href="http://coord.info/GC2PHWE"><img src="http://wampenschleifer.de/Logos/GC2PHWE.jpg" alt="GC2PHWE - Der Vorführer"></a>',  # Banner on special page
    'GC2PHWB': '<a href="http://coord.info/GC2PHWB"><img src="http://wampenschleifer.de/Logos/GC2PHWB.jpg" alt="GC2PHWB - Der Wachmann"></a>',  # Banner on special page
    'GC3REGY': '<a href="http://coord.info/GC3REGY"><img src="http://wampenschleifer.de/Logos/GC3REGY.jpg" alt="GC3REGY - Mäusepech - das Labyrinth"></a>',  # Banner on special page
    'GC2GJY9': '<a href="http://coord.info/GC2GJY9"><img src="http://wampenschleifer.de/Logos/GC2GJY9.jpg" alt="GC2GJY9 - Mäusejagd"></a>',  # Banner on special page
    'GC2YMKA': '<a href="http://coord.info/GC2YMKA"><img src="http://wampenschleifer.de/Logos/GC2YMKA.jpg" alt="GC2YMKA - Katzenklo, Katzenklo"></a>',  # Banner on special page
    'GC2KCRW': '<a href="http://coord.info/GC2KCRW"><img src="http://wampenschleifer.de/Logos/GC2KCRW.jpg" alt="GC2KCRW - Nicht mein Tag...?!"></a>',  # Banner on special page
    'GC26D16': '<a href="http://coord.info/GC26D16"><img src="http://wampenschleifer.de/Logos/GC26D16.jpg" alt="GC26D16 - Obmanns Spezialauftrag"></a>',  # Banner on special page
    'GC2FX2D': '<a href="http://coord.info/GC2FX2D"><img src="http://wampenschleifer.de/Logos/GC2FX2D.jpg" alt="GC2FX2D - Die Schlüssel des Schattenreichs"></a>',  # Banner on special page
    'GC3BZ1Q': '<a href="http://coord.info/GC3BZ1Q"><img src="http://wampenschleifer.de/Logos/GC3BZ1Q.jpg" alt="GC3BZ1Q - Das Märchen von der ZauberBoNe"></a>',  # Banner on special page
    'GC47M25': '<a href="http://coord.info/GC47M25"><img src="http://wampenschleifer.de/Logos/GC47M25.jpg" alt="GC47M25 - Atlantis"></a>',  # Banner on special page
    'GC511AX': '<a href="http://coord.info/GC511AX"><img src="http://wampenschleifer.de/Logos/GC511AX.jpg" alt="GC511AX - Rinderwahn"></a>',  # Banner on special page
    'GC537V1': '<a href="http://coord.info/GC537V1"><img src="http://wampenschleifer.de/Logos/GC537V1.jpg" alt="GC537V1 - Das Märchen vom Haveltroll"></a>',  # Banner on special page
    'GC5A4X9': '<a href="http://coord.info/GC5A4X9"><img src="http://wampenschleifer.de/Logos/GC5A4X9.jpg" alt="GC5A4X9 - Obmann - Der Lehrgang"></a>',  # Banner on special page
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
    'GC4YAEY': '<a href="http://coord.info/GC4YAEY"><img src="http://imgcdn.geocaching.com/cache/large/55fcadb9-4464-483c-b43a-8152cf51f422.jpg" width="468" border="0" height="344"></a>',  # Banner was deleted
    'GC4432N': None,  # NighT[131]TraiN : Bonus / reference to main cache looks like a banner
}


def collect_banner_urls(path_to_xml):
    banners = dict()
    for event, elem in cElementTree.iterparse(path_to_xml, events=[START_TAG, END_TAG]):
        if event == START_TAG and elem.tag == '{}wpt'.format(TOPO_NS):
            latitude = elem.get('lat')
            longitude = elem.get('lon')
        elif event == END_TAG and elem.tag == '{}name'.format(TOPO_NS):
            gc_code = elem.text
        elif event == END_TAG and elem.tag == '{}long_description'.format(GS_NAMESPACE):
            description = elem.text
            description = strip_pattern(description, r'((alt|title)=\".*?(>|<).*?\")')

            if gc_code in SPECIAL_BANNERS:
                banner = SPECIAL_BANNERS[gc_code]
            else:
                banner = parse_banner(description, gc_code)

            if banner:
                add_banner_to_dict(banner, banners)

        try:
            process_gc_data(gc_code, latitude, longitude)
        except NameError:
            pass

    return banners.values()


def add_banner_to_dict(banner, banner_dict):
    image = IMAGE_DECODED_PATTERN.search(banner)
    if image:
        image = image.group()
        src = SRC_PATTERN.search(image)
        if src:
            src = src.group()
            if src not in banner_dict:
                banner_dict[src] = banner


def parse_banner(description, gc_code):

    match = BANNER_ENCODED_PATTERN.search(description)
    if match:
        return normalize_banner(match.group())

    match = IMAGE_ENCODED_PATTERN.search(description)
    if match:
        return normalize_banner(match.group())

    matches = BANNER_DECODED_PATTERN.finditer(description)
    for match in matches:
        banner_probe = normalize_banner(match.group())
        if contains_cache_url(banner_probe, gc_code):
            return banner_probe

    description = description.replace('bannertype', '')
    match = LINKLESS_IMAGE_PATTERN.search(description)
    if match:
        return IMAGE_DECODED_PATTERN.search(match.group()).group()

    return None


def process_gc_data(gc_code, latitude, longitude):
    if gc_code and latitude and longitude:
        cache_coordinates = CacheCoordinates()
        cache_coordinates.gc_code = gc_code
        cache_coordinates.latitude = latitude
        cache_coordinates.longitude = longitude
        try:
            cache_coordinates.save()
        except:
            pass  # shut up


def normalize_banner(banner):
    banner = banner.replace('&lt;', '<')
    banner = banner.replace('&gt;', '>')
    banner = banner.replace('&amp;', '&')
    banner = banner.replace('\n', '')
    banner = banner.replace('<br />', ' ')
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


def contains_cache_url(banner_probe, gc_code):
    short_url = 'http://coord.info/' + gc_code
    long_url = 'geocaching.com/geocache/' + gc_code
    seek_url = 'geocaching.com/seek/cache_details.aspx?'

    if short_url in banner_probe:
        return True
    if long_url in banner_probe:
        return True
    if seek_url in banner_probe:
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
