from django.shortcuts import render

from .models import Cache


def downloads(request, cache_id):
    render_context = dict()
    render_context['id'] = cache_id

    cache = Cache.objects.get(cache_id=cache_id)
    if cache is None:
        render_context['errors'] = [_('Cache not found.')]
    else:
        render_context['name'] = cache.name
        render_context['downloads'] = cache.get_all_images()

    return render(request, 'downloads/downloads.html')


def create_downloads(request):
    pass
