# Generated by Django 5.0.3 on 2024-03-10 06:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0035_remove_user_ball"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telegram",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
    ]