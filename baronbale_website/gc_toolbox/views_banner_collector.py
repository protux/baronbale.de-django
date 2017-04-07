from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _

from . import banner_parser
from . import banner_sorter
from .forms import UploadGPXForm

BANNERS_SESSION_KEY = 'banners'
MARGIN_BETWEEN_BANNER = 3
CANVAS_WIDTH = 750


def index(request):
    upload_gpx_form = UploadGPXForm()
    request_dict = {
        'gpx_form': upload_gpx_form,
    }

    if request.session:
        banners = request.session.get(BANNERS_SESSION_KEY, None)
        request.session[BANNERS_SESSION_KEY] = None
        if banners:
            request_dict['banner'] = banners

    return render(request, 'gc_toolbox/banner_collector.html', request_dict)


def collect_banners(request):
    if request.method == 'POST':
        form = UploadGPXForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            gpx_file = form.cleaned_data['gpx_file']
            horizontal_banners_per_row = form.cleaned_data['horizontal_banners_per_row']
            vertical_banners_per_row = form.cleaned_data['vertical_banners_per_row']
            banners = banner_parser.collect_banner_urls(gpx_file)
            banners = banner_sorter.sort_banner(banners)
            joined_banners = join_banners(banners, horizontal_banners_per_row, vertical_banners_per_row)
            joined_banners += '<p>' + _(
                'The bannerlist was generated on') + ' <a href="https://baronbale.de/tools/gc/banner/">baronbale.de</a></p>'
            request.session[BANNERS_SESSION_KEY] = joined_banners

    return HttpResponseRedirect(reverse('gc_toolbox:banner_collector'))


def join_banners(banners, horizontal_banners_per_row, vertical_banners_per_row):
    joined_banners = ""
    balanced_output = False

    for idx, banner in enumerate(banners):
        if banner[banner_sorter.RATIO_TAG] > 1.0:  # if horizontal
            joined_banners += get_formatted_banner(banner, horizontal_banners_per_row) + '\n'
        elif not balanced_output and idx % horizontal_banners_per_row > 0 and banner[banner_sorter.RATIO_TAG] <= 1.0:
            joined_banners += get_formatted_banner(banner, horizontal_banners_per_row) + '\n'
            if idx % horizontal_banners_per_row == horizontal_banners_per_row - 1:
                balanced_output = True
        else:
            joined_banners += get_formatted_banner(banner, vertical_banners_per_row) + '\n'
            balanced_output = True

    return joined_banners + '\n'


def get_formatted_banner(banner, banner_per_row):
    return banner_parser.BANNER_TEMPLATE.format(
        banner[banner_parser.HREF_TAG],
        banner[banner_parser.SRC_TAG],
        calculate_banner_width(banner_per_row)
    )


def calculate_banner_width(banners_per_row):
    return int((CANVAS_WIDTH - ((banners_per_row - 1) * MARGIN_BETWEEN_BANNER)) / banners_per_row)
