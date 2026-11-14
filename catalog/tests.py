import json
import os
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase
from PIL import Image as PILImage

from catalog.models import Brand, Category, Customer, Product, WishList


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
        payload = response.json()[0]
        # Nested output per the assignment: Brand.name / Category.name
        self.assertEqual(payload['brand'], {'name': 'Rolex'})
        self.assertEqual(payload['category'], {'name': 'Dive Watches'})
        self.assertEqual(
            set(payload),
            {'id', 'title', 'slug', 'price', 'brand', 'category', 'is_available', 'stash'},
        )

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

    def test_create_product(self):
        payload = {
            'title': 'Seiko Prospex',
            'brand': self.brand.pk,
            'category': self.category.pk,
            'price': '5000000.00',
            'stash': 4,
        }
        response = self.client.post(
            '/api/products/create/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['slug'], 'seiko-prospex')
        self.assertTrue(Product.objects.filter(slug='seiko-prospex').exists())

    def test_wishlist_unique_together(self):
        user = User.objects.create_user('sara', 'sara@example.com', 'pass1234')
        customer = Customer.objects.create(user=user, phone_number='09120000000')
        WishList.objects.create(customer=customer, product=self.product)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                WishList.objects.create(customer=customer, product=self.product)

    def test_wishlist_requires_login_and_returns_nested_payload(self):
        anonymous = self.client.get('/api/me/wishlist/')
        self.assertEqual(anonymous.status_code, 403)

        user = User.objects.create_user('ali', 'ali@example.com', 'pass1234')
        customer = Customer.objects.create(user=user, phone_number='0912')
        WishList.objects.create(customer=customer, product=self.product)

        self.client.force_login(user)
        response = self.client.get('/api/me/wishlist/')
        self.assertEqual(response.status_code, 200)
        item = response.json()[0]
        self.assertEqual(item['product']['slug'], self.product.slug)
        self.assertEqual(
            item['customer'],
            {'username': 'ali', 'email': 'ali@example.com', 'phone_number': '0912'},
        )

    def test_create_product_with_uploaded_image(self):
        buffer = BytesIO()
        PILImage.new('RGB', (2, 2), 'red').save(buffer, format='PNG')
        upload = SimpleUploadedFile('watch.png', buffer.getvalue(), content_type='image/png')

        with tempfile.TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            response = self.client.post('/api/products/create/', data={
                'title': 'Seiko Presage',
                'brand': self.brand.pk,
                'category': self.category.pk,
                'price': '7000000.00',
                'stash': 2,
                'main_image': upload,
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn('media/products/watch.png', response.json()['main_image'])
            self.assertTrue(os.path.exists(os.path.join(media_root, 'products', 'watch.png')))
