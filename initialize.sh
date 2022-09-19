#!/usr/bin/env bash
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py makemigrations hysite
python3 manage.py migrate hysite