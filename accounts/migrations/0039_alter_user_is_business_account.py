# Generated by Django 5.0.3 on 2024-03-10 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0038_alter_user_is_business_account"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_business_account",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
