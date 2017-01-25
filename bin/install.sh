#!/bin/bash
INSTALL_FILE=/home/nico/baronbale.de_install.tar.xz 

source ve_baronbale.de/bin/activate

echo 'stopping server...'
uwsgi --stop /var/run/baronbale.de.pid

echo 'updating server...'
tar -xJf $INSTALL_FILE --overwrite
sed -i 's/DEBUG = True/DEBUG = False/g' baronbale_website/baronbale_website/settings.py
python baronbale_website/manage.py collectstatic --noinput
python baronbale_website/manage.py migrate

echo 'changing owner...'
chown -R www-data:www-data ./*
chown -R www-data:www-data /var/www/baronbale.de/

echo 'starting server...'
uwsgi --ini uwsgi.ini

echo 'cleaning up...'
rm -f $INSTALL_FILE

echo 'done.' 
