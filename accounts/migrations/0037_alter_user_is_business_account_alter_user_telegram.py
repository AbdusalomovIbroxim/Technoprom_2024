# Generated by Django 5.0.3 on 2024-03-10 07:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0036_alter_user_telegram"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_business_account",
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="telegram",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
