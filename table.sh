#!/usr/bin/env bash

# 初始化表
python3 manage.py makemigrations hysite
python3 manage.py migrate hysite
