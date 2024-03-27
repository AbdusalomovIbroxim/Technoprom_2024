# Generated by Django 4.2.2 on 2023-09-15 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='films',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product-about_us/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.films')),
            ],
        ),
    ]
