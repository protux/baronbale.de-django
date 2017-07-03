from django.conf.urls import url

from . import views

app_name = 'checker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^correct$', views.correct, name='correct'),
    url(r'^incorrect$', views.incorrect, name='incorrect'),
]
