from django.conf.urls import url

from . import views

app_name = "toolbox"
urlpatterns = (
    url(r"duplicateremover/", views.duplicate_remover, name="duplicate_remover"),
)
