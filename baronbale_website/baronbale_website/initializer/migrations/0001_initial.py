from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

def set_site_name(apps, schema_editor):
    Site = apps.get_model("sites", "site")
    site = Site()

    site.name = "baronbale.de"
    if settings.DEBUG:
        site.domain = "localhost:8000"
    else:
        site.domain = "baronbale.de"
    site.save()

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]
    
    operations = [
        migrations.RunPython(set_site_name),
    ]
