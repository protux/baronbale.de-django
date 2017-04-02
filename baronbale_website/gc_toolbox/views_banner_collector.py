from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _

from . import banner_parser
from . import banner_sorter
from .forms import UploadGPXForm

BANNERS_SESSION_KEY = 'banners'


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
            banners = banner_parser.collect_banner_urls(gpx_file)
            banners = banner_sorter.sort_banner(banners)
            joined_banners = "\n".join([get_banner_from_dict(banner) for banner in banners]) + '\n'
            joined_banners += '<p>' + _(
                'The bannerlist was generated on') + ' <a href="https://baronbale.de/tools/gc/banner/">baronbale.de</a></p>'
            request.session[BANNERS_SESSION_KEY] = joined_banners

    return HttpResponseRedirect(reverse('gc_toolbox:banner_collector'))


def get_banner_from_dict(banner_dict):
    return banner_parser.BANNER_TEMPLATE.format(
        banner_dict[banner_parser.HREF_TAG],
        banner_dict[banner_parser.SRC_TAG]
    )
