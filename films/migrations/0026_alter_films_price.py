# Generated by Django 4.2.2 on 2023-10-22 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0025_alter_films_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='films',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]
