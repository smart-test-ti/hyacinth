#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
from logzero import logger
import platform

def dbInitialize():
    """db config initialize"""
    content = {
        'db_name': 'none',
        'db_host': 'none',
        'db_port': 'none',
        'db_user': 'none',
        'db_password': 'none'
    }
    if not os.path.exists('./hyacinth/config.json'):
       if not os.path.exists('hyacinth'):
           os.mkdir('hyacinth')
       with open('./hyacinth/config.json', 'a+', encoding="utf-8") as file:
           file.write(json.dumps(content))

def checkPyVer():
    """check python version"""
    if int(platform.python_version().split('.')[0]) < 3:
        logger.error('python version must be >2,your python version is {}'.format(platform.python_version()))
        logger.error('please install python::3 and pip3 install -U solox')
        sys.exit()

def main():
    """Run administrative tasks."""
    checkPyVer()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hyacinth.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
