#!/usr/bin/bash

source ve_baronbale.de/bin/activate
cd baronbale_website
python manage.py makemessages -l de
cd ..

cp baronbale_website/gc_toolbox/locale/de/LC_MESSAGES/django.po localize_project/source/gc_toolbox.po
cp baronbale_website/staticpages/locale/de/LC_MESSAGES/django.po localize_project/source/staticpages.po
cp baronbale_website/toolbox/locale/de/LC_MESSAGES/django.po localize_project/source/toolbox.po
cp baronbale_website/homepage/locale/de/LC_MESSAGES/django.po localize_project/source/homepage.po
cp baronbale_website/templates/locale/de/LC_MESSAGES/django.po localize_project/source/templates.po
