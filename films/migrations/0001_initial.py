# Generated by Django 4.2.2 on 2023-09-13 11:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Город',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страна',
            },
        ),
        migrations.CreateModel(
            name='SubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Субкатегория')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.categories')),
            ],
            options={
                'verbose_name': 'Субкатегория',
                'verbose_name_plural': 'Субкатегории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='films.categories')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='films.subcategories')),
            ],
        ),
        migrations.CreateModel(
            name='Films',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('telephone', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('email', models.CharField(max_length=100, verbose_name='Емайл адрес')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product-about_us/', verbose_name='Картинка')),
                ('view_count', models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('is_active', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='buy', max_length=50)),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.categories')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='films.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.country')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.subcategories')),
                ('tags', models.ManyToManyField(blank=True, to='films.tag')),
            ],
            options={
                'verbose_name': 'Запрос',
                'verbose_name_plural': 'Запросы',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.country'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='films.films')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.films')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product_id')},
            },
        ),
    ]
