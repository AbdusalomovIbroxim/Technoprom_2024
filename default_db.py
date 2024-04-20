import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

from films.models import Categories, SubCategories, Tag, Country, City, SubCategoryCategory, TagCategory, TagSubcategory

from django.db import IntegrityError


def load_from_json_and_save_to_database(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for category_data in data.get('categories', []):
        Categories.objects.get_or_create(**category_data)

    for subcategory_data in data.get('subcategories', []):
        SubCategories.objects.get_or_create(**subcategory_data)

    for tag_data in data.get('tags', []):
        Tag.objects.get_or_create(**tag_data)

    try:
        for country_data in data.get('countries', []):
            Country.objects.get_or_create(**country_data)
    except IntegrityError as e:
        print(f"Error adding countries: {e}")

    try:
        for city_data in data.get('cities', []):
            City.objects.get_or_create(**city_data)
    except IntegrityError as e:
        print(f"Error adding cities: {e}")

    try:
        for subcategory_category_data in data.get('subcategory_category', []):
            SubCategoryCategory.objects.get_or_create(**subcategory_category_data)
    except IntegrityError as e:
        print(f"Error adding subcategory_category: {e}")

    try:
        for tag_category_data in data.get('tag_category', []):
            TagCategory.objects.get_or_create(**tag_category_data)
    except IntegrityError as e:
        print(f"Error adding tag_category: {e}")

    try:
        for tag_subcategory_data in data.get('tag_subcategory', []):
            TagSubcategory.objects.get_or_create(**tag_subcategory_data)
    except IntegrityError as e:
        print(f"Error adding tag_subcategory: {e}")


if __name__ == "__main__":
    file_path = './data.json'
    load_from_json_and_save_to_database(file_path)
    print(f'Данные успешно загружены в базу данных.')
