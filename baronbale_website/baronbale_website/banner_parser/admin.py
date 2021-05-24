from django.contrib import admin

from baronbale_website.banner_parser import models


class EnqueuedJobAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_id",
        "email_address_to_notify",
        "uploaded_file",
        "time_created",
        "time_finished",
    )


class BannerDimensionAdmin(admin.ModelAdmin):
    list_display = ("gc_code", "ratio", "url")


class BannerCacheAdmin(admin.ModelAdmin):
    list_display = ("gc_code", "reason", "image_url", "permanent")


admin.site.register(models.BannerParserJob, EnqueuedJobAdmin)
admin.site.register(models.BannerDimension, BannerDimensionAdmin)
admin.site.register(models.BannerCache, BannerCacheAdmin)
