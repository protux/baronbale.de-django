#!/usr/bin/bash
find . -name __pycache__ | xargs rm -rf
mv baronbale_website/db.sqlite3 .
tar --create -f baronbale.de_install.tar.xz --xz baronbale_website/ bin/ static/ pip_dependency_list/
scp -P 8965 baronbale.de_install.tar.xz 195.201.94.237:/home/nico/
mv ./db.sqlite3 baronbale_website/
rm -f baronbale.de_install.tar.xz
