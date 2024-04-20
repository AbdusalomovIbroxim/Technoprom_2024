#!/usr/bin/.env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

        # Проверяем наличие данных о категориях и вызываем функцию добавления категорий, если данные отсутствуют
        # from default_db import add_categories, add_subcategories, add_tags, add_countries, add_cities
        # add_categories()
        # add_subcategories()
        # add_tags()
        # add_countries()
        # add_cities()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()
