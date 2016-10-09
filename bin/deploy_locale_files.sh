#!/usr/bin/bash

cp localize_project/target/gc_toolbox.po baronbale_website/gc_toolbox/locale/de/LC_MESSAGES/django.po
cp localize_project/target/staticpages.po baronbale_website/staticpages/locale/de/LC_MESSAGES/django.po
cp localize_project/target/toolbox.po baronbale_website/toolbox/locale/de/LC_MESSAGES/django.po
cp localize_project/target/homepage.po baronbale_website/homepage/locale/de/LC_MESSAGES/django.po
cp localize_project/target/templates.po baronbale_website/templates/locale/de/LC_MESSAGES/django.po

source ve_baronbale.de/bin/activate
cd baronbale_website
python manage.py compilemessages
