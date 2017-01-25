from django.conf.urls import url

from . import views

app_name = 'lab'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^json/$', views.display_json, name='json'),
]
