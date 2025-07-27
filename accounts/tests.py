from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Restaurant, Product, Client as ClientProfile, CartItem, Order

User = get_user_model()


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_client_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'role': 'client',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        user = User.objects.create_user(username='loginuser', password='Testpass123!', is_client=True)
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)


class RestaurantTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employee', password='Testpass123!', is_employee=True)
        self.client = Client()
        self.client.login(username='employee', password='Testpass123!')

    def test_add_restaurant(self):
        response = self.client.post(reverse('add_restaurant'), {
            'name': 'Test Restaurant',
            'address': 'Sofia'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Restaurant.objects.count(), 1)


class ProductTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='R1', address='Sofia')
        self.user = User.objects.create_user(username='employee', password='Testpass123!', is_employee=True)
        self.client = Client()
        self.client.login(username='employee', password='Testpass123!')

    def test_add_product(self):
        response = self.client.post(reverse('add_product'), {
            'restaurant': self.restaurant.id,
            'name': 'Burger',
            'description': 'Tasty',
            'price': 10,
            'category': 'pizza'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client', password='Testpass123!', is_client=True)
        self.client_profile = ClientProfile.objects.create(user=self.user, address='Test Address')
        self.product = Product.objects.create(
            name='Pizza',
            description='Hot',
            price=12,
            category='food',
            restaurant=Restaurant.objects.create(name='R2', address='Plovdiv')
        )
        self.client_instance = Client()
        self.client_instance.login(username='client', password='Testpass123!')

    def test_add_to_cart(self):
        response = self.client_instance.get(reverse('add_to_cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 1)

    def test_view_cart(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        response = self.client_instance.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza')


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client', password='Testpass123!', is_client=True)
        self.client_profile = ClientProfile.objects.create(user=self.user, address='Test Address')
        self.client_instance = Client()
        self.client_instance.login(username='client', password='Testpass123!')
        self.restaurant = Restaurant.objects.create(name='R3', address='Burgas')
        self.product = Product.objects.create(name='Sushi', description='Fresh', price=15,
                                              category='food', restaurant=self.restaurant)
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

    def test_checkout_page_loads(self):
        response = self.client_instance.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        response = self.client_instance.post(reverse('checkout'), {
            'address': 'Client Address',
            'phone_number': '0888123456'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.filter(client=self.client_profile).count(), 1)

class TrackOrdersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client2', password='Testpass123!', is_client=True)
        self.client_profile = ClientProfile.objects.create(user=self.user, address='Some Address')
        self.client_instance = Client()
        self.client_instance.login(username='client2', password='Testpass123!')

    def test_track_orders_page_loads(self):
        response = self.client_instance.get(reverse('track_orders'))
        self.assertEqual(response.status_code, 200)
