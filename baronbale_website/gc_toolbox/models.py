from django.db import models


class CacheCoordinates(models.Model):
    gc_code = models.CharField(max_length=10)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)

    class Meta:
        unique_together = (('gc_code', 'latitude', 'longitude'),)
