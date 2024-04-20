from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode
from django.db.models import (
    Model,
    CharField,
    SlugField,
    CASCADE,
    ForeignKey,
    DateTimeField,
    BooleanField,
    PositiveBigIntegerField,
    ImageField,
    SET_NULL,
    ManyToManyField,
    PositiveIntegerField,
    FloatField,
)
from django.urls import reverse_lazy
from django.utils.translation.trans_real import get_language


class Categories(Model):
    slug = SlugField(unique=True)
    name_en = CharField("Category (English)", max_length=50, default="")
    name_ru = CharField("Категория (Русский)", max_length=50, default="")
    name_uz = CharField("Kategoriya (O'zbek)", max_length=50, default="")
    is_linked = BooleanField(default=False)

    def __str__(self):
        language_code = get_language()
        if language_code == "uz":
            return self.name_ru
        elif language_code == "ru":
            return self.name_ru
        elif language_code == "en":
            return self.name_en
        else:
            return self.name_en

    def get_absolute_url(self):
        return reverse_lazy("category_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategories(Model):
    slug = SlugField(unique=True)
    name_en = CharField("Subcategory (English)", max_length=100, default="")
    name_ru = CharField("Подкатегория (Русский)", max_length=100, default="")
    name_uz = CharField("Subkategoriya (O'zbek)", max_length=100, default="")
    is_linked = BooleanField(default=False)

    def __str__(self):
        language_code = get_language()
        if language_code == 'uz':
            return self.name_uz
        elif language_code == 'ru':
            return self.name_ru
        elif language_code == 'en':
            return self.name_en
        else:
            return self.name_en

    def get_absolute_url(self):
        return reverse_lazy("subcategory_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"


class SubCategoryCategory(Model):
    subcategory = ForeignKey(SubCategories, on_delete=CASCADE)
    category = ForeignKey(Categories, on_delete=CASCADE)


class Tag(Model):
    name_en = CharField("Tag Name (English)", max_length=255, unique=True, default="")
    name_ru = CharField("Имя тега (Русский)", max_length=255, unique=True, default="")
    name_uz = CharField("Tag nomi (O'zbek)", max_length=255, unique=True, default="")
    is_linked = BooleanField(default=False)

    def __str__(self):
        language_code = get_language()
        if language_code == 'uz':
            return self.name_uz
        elif language_code == 'ru':
            return self.name_ru
        elif language_code == 'en':
            return self.name_en
        else:
            return self.name_en


class TagCategory(Model):
    category = ForeignKey(Categories, on_delete=CASCADE, related_name="tags")
    tag = ForeignKey(Tag, on_delete=CASCADE, related_name="category_tags", db_column="tag__category")


class TagSubcategory(Model):
    subcategory = ForeignKey(SubCategories, on_delete=CASCADE, related_name="tags")
    tag = ForeignKey(Tag, on_delete=CASCADE, related_name="subcategory_tags", db_column="tag__subcategory")


class Country(Model):
    slug = SlugField(unique=True)
    name_en = CharField("Country (English)", max_length=50, default="")
    name_ru = CharField("Страна (Русский)", max_length=50, default="")
    name_uz = CharField("Davlat (O'zbek)", max_length=50, default="")

    def __str__(self):
        language_code = get_language()
        if language_code == 'en':
            return self.name_en
        elif language_code == 'ru':
            return self.name_ru
        elif language_code == 'uz':
            return self.name_uz
        else:
            return self.name_uz

    def get_absolute_url(self):
        language_code = get_language()
        if language_code == 'en':
            return reverse_lazy("country_detail", kwargs={"slug": self.slug})
        elif language_code == 'ru':
            return reverse_lazy("country_detail_ru", kwargs={"slug": self.slug})
        elif language_code == 'uz':
            return reverse_lazy("country_detail_uz", kwargs={"slug": self.slug})
        else:
            return reverse_lazy("country_detail",
                                kwargs={"slug": self.slug})  # По умолчанию возвращаем английскую ссылку

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class City(Model):
    slug = SlugField(unique=True)
    country = ForeignKey(Country, on_delete=CASCADE)
    name = CharField("Город", max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("city_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Город"


class Products(Model):  # Модель
    TYPE_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    slug = SlugField(unique=True)
    title = CharField("Наименование", max_length=100)
    description = CharField("Описание", max_length=900, null=True, blank=True)
    # image = ImageField(
    #     upload_to="product-about_us/",
    #     blank=True,
    #     null=True,
    #     default="product-about_us/image.png",
    # )
    telephone = CharField("Номер телефона", max_length=30)
    telephone_view_count = PositiveBigIntegerField(
        "Количество просмотров номер телефона", default=0
    )
    telegram = CharField("Телеграмм номер", max_length=100, blank=True, null=True)
    # email = CharField("Емайл адрес", max_length=100)
    view_count = PositiveBigIntegerField("Количество просмотров", default=0)
    create_date = DateTimeField("Дата создания", auto_now_add=True)
    update_date = DateTimeField("Дата обновления", auto_now=True)
    is_published = BooleanField("Опубликовано", default=True)
    country = ForeignKey(Country, on_delete=CASCADE)
    city = ForeignKey(City, on_delete=CASCADE, blank=True, null=True)
    category = ForeignKey(Categories, CASCADE)
    subcategories = ManyToManyField(SubCategories, blank=True)
    tags = ManyToManyField(Tag, blank=True)
    is_active = BooleanField(default=False)
    type = CharField(max_length=50, choices=TYPE_CHOICES, default="buy")
    author = ForeignKey(get_user_model(), SET_NULL, blank=True, null=True)
    price = FloatField("Цена", blank=True, null=True)
    is_price_negotiable = BooleanField("Договорная цена", default=False)
    is_top_film = BooleanField(default=False)
    top_duration = PositiveIntegerField("Продолжительность в топе (в днях)", default=0)
    create_date_changed = BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:  # Check if slug is not already set
            # Convert non-Latin characters to Latin characters
            latin_title = unidecode(self.title)
            self.slug = slugify(latin_title)  # Generate slug based on Latin title

            # Ensure uniqueness of the slug
            original_slug = self.slug
            counter = 1
            while Products.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(original_slug, counter)
                counter += 1

        # Set is_top_film based on top_duration
        self.is_top_film = self.top_duration > 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"


class Image(Model):
    image = ImageField(upload_to='product-about_us', default='product-about_us/default.jpg')
    product = ForeignKey("films.Products", on_delete=CASCADE)


# class ProductSubcategories(Model):
#     subCategory = ForeignKey("films.SubCategories", on_delete=CASCADE)
#     product = ForeignKey("films.Products", on_delete=CASCADE)
#
#
# class ProductTag(Model):
#     subCategory = ForeignKey("films.Tag", on_delete=CASCADE)
#     product = ForeignKey("films.Products", on_delete=CASCADE)


class Favorite(Model):
    user = ForeignKey(get_user_model(), CASCADE)
    product_id = ForeignKey(Products, CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product_id")

    def __str__(self):
        return f"{self.user}, {self.product_id_id}"
