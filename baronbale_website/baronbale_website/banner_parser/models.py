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
