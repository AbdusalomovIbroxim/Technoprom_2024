# Generated by Django 4.2.2 on 2023-10-10 11:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films', '0016_rename_favorite_user_favorite'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_favorite',
            new_name='UserFavorite',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
