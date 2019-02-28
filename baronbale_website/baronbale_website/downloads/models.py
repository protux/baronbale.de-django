from django.db import models
from django.utils.translation import ugettext as _


class Cache(models.Model):
    cache_id = models.CharField(_('Cache-ID'))
    name = models.CharField(_('Cache-Name'))

    def get_all_images(self):
        return DownloadFile.objects.filter(cache=self)


class DownloadFile(models.Model):
    name = models.CharField(_('name'))
    download_file = models.FileField(_('Download-File'), upload_to='downloads/')
    cache = models.ForeignKeyField(
        Cache,
        models.CASCADE,
        null=False,
        blank=False
    )
