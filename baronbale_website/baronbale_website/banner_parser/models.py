from django.db import models
from django.utils.translation import gettext as _

from baronbale_website.banner_parser.generators import ticket_id_generator


class EnqueuedBannerParserJob(models.Model):
    ticket_id = models.CharField(
        max_length=100, default=ticket_id_generator.generate_ticket_id
    )
    email_address_to_notify = models.CharField(null=True, blank=True, max_length=100)
    uploaded_file = models.FileField(verbose_name=_("GPX-File or Zip Archive"))
    time_created = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)
    time_finished = models.DateTimeField(null=True, blank=True)


class BannerDimension(models.Model):
    gc_code = models.CharField(max_length=20)
    banner = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    ratio = models.FloatField(default=0.0)
    width = models.IntegerField()
    height = models.IntegerField()


class BannerCache(models.Model):
    gc_code = models.CharField(max_length=10)
    image_url = models.CharField(max_length=1024, null=True, blank=True)
    reason = models.CharField(max_length=100)
    permanent = models.BooleanField(default=False)
