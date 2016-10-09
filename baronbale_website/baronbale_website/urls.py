"""baronbale_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from django_xmlrpc.views import handle_xmlrpc

urlpatterns = i18n_patterns(
	url(r'^tools/gc/', include('gc_toolbox.urls')),
    url(r'^tools/', include('toolbox.urls')),
    url(r'^blog/', include('zinnia.urls')),
    url(r'blog/comments/', include('django_comments.urls')),
    url(r'blog/rss/', RedirectView.as_view(url=reverse_lazy('zinnia:entry_feed')), name='rss_redirect'),
    url(r'^', include('homepage.urls')),
    url(r'^blog/xmlrpc/$', handle_xmlrpc),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('staticpages.urls')),
)

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404 = 'staticpages.views.error404'
