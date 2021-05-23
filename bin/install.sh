#!/bin/bash
INSTALL_FILE=/home/nico/baronbale.de_install.tar.xz 

source venv/bin/activate

echo 'stopping server...'
uwsgi --stop /var/run/baronbale.de.pid

echo 'updating server...'
pip install -U pip wheel setuptools
pip install -r requirements.txt
tar -xJf $INSTALL_FILE --overwrite
python baronbale_website/manage.py collectstatic --noinput
python baronbale_website/manage.py migrate

echo 'changing owner...'
chown -R www-data:www-data ./*
chown -R www-data:www-data /var/www/baronbale.de/

echo 'starting server...'
source .env
uwsgi --ini uwsgi.ini

echo 'cleaning up...'
rm -f $INSTALL_FILE

echo 'done.' 
