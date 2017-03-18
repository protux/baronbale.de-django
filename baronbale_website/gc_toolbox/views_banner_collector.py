from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import banner_parser
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
            banner = banner_parser.collect_banner_urls(gpx_file)
            request.session[BANNERS_SESSION_KEY] = "\n".join(banner)
    return HttpResponseRedirect(reverse('gc_toolbox:banner_collector'))
