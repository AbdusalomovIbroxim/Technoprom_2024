# Generated by Django 4.2.2 on 2023-10-07 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_userrating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userrating',
            unique_together={('rater', 'rated_user')},
        ),
    ]
