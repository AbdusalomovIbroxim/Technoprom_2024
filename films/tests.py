from django.test import TestCase
from .models import Products, Categories, Country


class ProductsTestCase(TestCase):
    def setUp(self):
        category = Categories.objects.create(name_ru="Тестовая категория")
        country = Country.objects.create(name_ru="Тестовая страна")
        Products.objects.create(title="Тестовый продукт", description="Тестовое описание", category=category,
                                country=country)

    def test_product_creation(self):
        product = Products.objects.get(title="Тестовый продукт")
        self.assertEqual(product.description, "Тестовое описание")
