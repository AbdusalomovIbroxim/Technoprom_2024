# Generated by Django 4.2.2 on 2023-09-20 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_films_image_delete_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='films',
            name='image',
            field=models.ImageField(blank=True, default='product-about_us/image.png', null=True, upload_to='product-about_us/'),
        ),
    ]
