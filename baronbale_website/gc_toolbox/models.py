from django.db import models


class CacheCoordinates(models.Model):
    gc_code = models.CharField(max_length=10)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)
    type = models.CharField(max_length=30, null=True)

    class Meta:
        unique_together = (('gc_code', 'latitude', 'longitude'),)


class BannerDimension(models.Model):
    banner = models.CharField(max_length=64)
    ratio = models.FloatField(default=0.0)
    width = models.IntegerField()
    height = models.IntegerField()
