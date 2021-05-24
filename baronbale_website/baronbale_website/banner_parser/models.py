from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator

from baronbale_website.banner_parser.generators import ticket_id_generator


class BannerParserJob(models.Model):
    ticket_id = models.CharField(
        max_length=20, default=ticket_id_generator.generate_ticket_id
    )
    email_address_to_notify = models.CharField(null=True, blank=True, max_length=100)
    uploaded_file = models.FileField(verbose_name=_("GPX-File or Zip Archive"))
    horizontal_banners_per_row = models.IntegerField(validators=[MinValueValidator(1)])
    vertical_banners_per_row = models.IntegerField(validators=[MinValueValidator(1)])
    time_created = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)
    time_finished = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Banner Parser Job #{self.ticket_id}"


class BannerDimension(models.Model):
    gc_code = models.CharField(max_length=20)
    banner = models.CharField(max_length=64)
    url = models.CharField(max_length=1024)
    ratio = models.FloatField(default=0.0)
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self) -> str:
        return f"Dimensions of {self.gc_code}'s Banner"


class BannerCache(models.Model):
    gc_code = models.CharField(max_length=10)
    image_url = models.CharField(max_length=1024, null=True, blank=True)
    reason = models.CharField(max_length=100)
    permanent = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Banner for {self.gc_code}"
