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
from django.urls import path
from django.conf import settings
from django.contrib import admin

urlpatterns = i18n_patterns(
    path("banners/", include("baronbale_website.banner_parser.urls")),
    url(r"^tools/gc/", include("baronbale_website.gc_toolbox.urls")),
    url(r"^tools/", include("baronbale_website.toolbox.urls")),
    url(r"^", include("baronbale_website.homepage.urls")),
    url(r"^o_pulchram_avem/", include("baronbale_website.checker.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^", include("baronbale_website.staticpages.urls")),
)

urlpatterns += [
    url(r"^i18n/", include("django.conf.urls.i18n")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'staticpages.views.error404'
