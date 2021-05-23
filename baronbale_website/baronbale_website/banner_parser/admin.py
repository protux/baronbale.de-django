from django.contrib import admin

from baronbale_website.banner_parser import models


class EnqueuedJobAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'email_address_to_notify', 'uploaded_file', 'time_created',)


admin.site.register(models.EnqueuedBannerParserJob, EnqueuedJobAdmin)
