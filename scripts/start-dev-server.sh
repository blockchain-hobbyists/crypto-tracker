#!/bin/bash

python manage.py migrate
python manage.py upsert_all_meta
python manage.py runserver 0.0.0.0:"$PORT"
