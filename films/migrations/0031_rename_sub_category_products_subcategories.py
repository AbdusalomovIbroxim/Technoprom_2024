# Generated by Django 4.2.7 on 2024-03-03 12:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("films", "0030_alter_products_sub_category_alter_products_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="products",
            old_name="sub_category",
            new_name="subcategories",
        ),
    ]
