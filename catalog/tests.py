from django.test import TestCase

from catalog.models import Brand, Category, Product


class ProductAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Rolex')
        cls.category = Category.objects.create(title='Dive Watches')
        cls.product = Product.objects.create(
            title='Submariner',
            brand=cls.brand,
            category=cls.category,
            price='10000.00',
            is_special=True,
            is_luxury=True,
            stash=3,
        )
        Product.objects.create(
            title='Speedmaster',
            brand=cls.brand,
            category=cls.category,
            price='20000.00',
            is_special=True,
            is_luxury=True,
        )

    def test_product_list_uses_one_query(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['brand'], 'Rolex')

    def test_luxury_list_uses_one_query_with_average(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/luxury-special/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item['average_luxury_price'] for item in response.json()},
            {'15000.00'},
        )

    def test_detail_increments_click_count(self):
        response = self.client.get(f'/api/products/{self.product.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['click_count'], 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.click_count, 1)

    def test_unknown_slug_returns_404_without_increment(self):
        response = self.client.get('/api/products/does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.product.refresh_from_db()
        self.assertEqual(self.product.click_count, 0)
