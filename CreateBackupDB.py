import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

# Импортируем модели
from films.models import Categories, SubCategories, Tag, Country, City, SubCategoryCategory, TagCategory, TagSubcategory


def export_to_json(file_path):
    data = {}

    categories_data = list(Categories.objects.all().values())
    data['categories'] = categories_data

    subcategories_data = list(SubCategories.objects.all().values())
    data['subcategories'] = subcategories_data

    tags_data = list(Tag.objects.all().values())
    data['tags'] = tags_data

    countries_data = list(Country.objects.all().values())
    data['countries'] = countries_data

    cities_data = list(City.objects.all().values())
    data['cities'] = cities_data

    subcategory_category_data = list(SubCategoryCategory.objects.all().values())
    data['subcategory_category'] = subcategory_category_data

    tag_category_data = list(TagCategory.objects.all().values())
    data['tag_category'] = tag_category_data

    tag_subcategory_data = list(TagSubcategory.objects.all().values())
    data['tag_subcategory'] = tag_subcategory_data

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    file_path = 'data.json'
    if os.path.exists(file_path):
        print(f'Файл {file_path} уже существует. Перезаписать его? (yes/no)')
        choice = input().lower()
        if choice != 'yes':
            print('Отменено.')
            exit()

    export_to_json(file_path)
    print(f'Данные успешно экспортированы в {file_path}.')
