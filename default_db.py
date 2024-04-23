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
        try:
            Categories.objects.create(**category_data)
        except IntegrityError as e:
            print(f"Error adding category: {e}")

    for subcategory_data in data.get('subcategories', []):
        try:
            SubCategories.objects.create(**subcategory_data)
        except IntegrityError as e:
            print(f"Error adding subcategory: {e}")

    for tag_data in data.get('tags', []):
        try:
            Tag.objects.create(**tag_data)
        except IntegrityError as e:
            print(f"Error adding tag: {e}")

    for country_data in data.get('countries', []):
        try:
            Country.objects.create(**country_data)
        except IntegrityError as e:
            print(f"Error adding country: {e}")

    for city_data in data.get('cities', []):
        try:
            City.objects.create(**city_data)
        except IntegrityError as e:
            print(f"Error adding city: {e}")

    for subcategory_category_data in data.get('subcategory_category', []):
        try:
            SubCategoryCategory.objects.create(**subcategory_category_data)
        except IntegrityError as e:
            print(f"Error adding subcategory category: {e}")

    for tag_category_data in data.get('tag_category', []):
        try:
            TagCategory.objects.get_or_create(**tag_category_data)
        except IntegrityError as e:
            print(f"Error adding tag category: {e}")

    for tag_subcategory_data in data.get('tag_subcategory', []):
        try:
            TagSubcategory.objects.get_or_create(**tag_subcategory_data)
        except IntegrityError as e:
            print(f"Error adding tag subcategory: {e}")


if __name__ == "__main__":
    file_path = './data.json'
    load_from_json_and_save_to_database(file_path)
    print(f'Данные успешно загружены в базу данных.')
