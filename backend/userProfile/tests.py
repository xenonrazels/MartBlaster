from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from store.models import Product, OrderItem, Order,Category
from .forms import ProductForm


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword' 
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_vendor_detail(self):
        response = self.client.get(reverse('userProfile:vendor_detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_my_account(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('userProfile:my_account'))
        self.assertEqual(response.status_code, 200)

    def test_my_store(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('userProfile:my_store'))
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        self.client.force_login(self.user)
        category = Category.objects.create(title='Test Category')
        response = self.client.post(reverse('userProfile:add_product'), {
            'title': 'Test Product',
            'description': 'This is a test product.',
            'price': 10,
            'image': 'test.png',
            'category':category.id


        })
        self.assertEqual(response.status_code, 302)
      

    def test_edit_product(self):
        self.client.force_login(self.user)
        category = Category.objects.create(title='Test Category`')

        product = Product.objects.create(
            title='Test Product',
            description='This is a test product.',
            price=10,
            added_by=self.user,
            category=category.id

        )
        response = self.client.post(reverse('userProfile:edit_product', args=[product.id]), {
            'title': 'Edited Product',
            'description': 'This is an edited product.',
            'price': 20,
            'image': 'test.png',
            'category':category.id
        })
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.title, 'Edited Product')
        self.assertEqual(product.price, 20)

