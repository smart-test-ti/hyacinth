#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json


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

def main():
    """Run administrative tasks."""
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
