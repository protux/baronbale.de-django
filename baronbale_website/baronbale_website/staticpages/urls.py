from django.conf.urls import url

from . import views

app_name = "staticpages"
urlpatterns = [
    url(r"contribute/$", views.Contribute.as_view(), name="contribute"),
    url(r"imprint/$", views.Imprint.as_view(), name="imprint"),
    url(r"privacy/$", views.PrivacyPolicy.as_view(), name="privacy"),
    url(r"roadmap/$", views.Roadmap.as_view(), name="roadmap"),
]
