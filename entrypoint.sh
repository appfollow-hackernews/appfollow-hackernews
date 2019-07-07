#!/bin/sh

if [ "$1" == "backend" ]; then
    ./manage.py migrate
    ./manage.py runserver 0.0.0.0:8000
elif [ "$1" == "worker" ]; then
    ./manage.py migrate
    celery -A appfollow_hackernews worker -B
fi