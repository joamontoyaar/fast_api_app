#!/bin/sh                   # This is a shell executable that runs the file

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"              