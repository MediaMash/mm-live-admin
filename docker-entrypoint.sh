#!/bin/bash

# It is responsability of the deployment orchestration to execute before
# migrations, create default admin user, populate minimal data, etc.
echo $(date -u) "- Migrating"
python manage.py makemigrations
python manage.py migrate


gunicorn video_service.wsgi --config video_service/gunicorn_conf.py
