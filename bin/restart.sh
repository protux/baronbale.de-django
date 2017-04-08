#!/bin/bash

echo 'stopping server...'
uwsgi --stop /var/run/baronbale.de.pid

echo 'starting server...'
uwsgi --ini uwsgi.ini
