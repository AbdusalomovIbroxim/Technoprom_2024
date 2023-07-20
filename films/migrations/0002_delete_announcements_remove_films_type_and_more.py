# Generated by Django 4.2.2 on 2023-06-21 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Announcements',
        ),
        migrations.RemoveField(
            model_name='films',
            name='type',
        ),
        migrations.AlterField(
            model_name='films',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='films.categories'),
        ),
        migrations.AlterField(
            model_name='films',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.subcategories'),
        ),
    ]
