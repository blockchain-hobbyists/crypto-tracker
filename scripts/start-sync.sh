#!/bin/bash

python manage.py migrate
python manage.py update_pairs_prices --infinite-run
