#!/bin/sh

cd /diaryspace
python manage.py makemigrations
python manage.py migrate
python manage.py runserver