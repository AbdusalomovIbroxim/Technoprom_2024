# Generated by Django 4.2.2 on 2023-06-26 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_films_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='films',
            name='author',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
