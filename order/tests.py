from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime
from .models import Product, Order, Quantity
from .serilizers import ProductSerializer, OrderSerializer, QuantitySerializer

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Test Product',
            'price': 10,
            'img': 'test.jpg',
            'description': 'Test description',
            'category': Product.Category.MAIN,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(pk=response.data['id'])
        self.assertEqual(product.name, 'Test Product')

    def test_retrieve_product(self):
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )
        url = reverse('product-detail', args=[product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_update_product(self):
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )
        url = reverse('product-detail', args=[product.id])
        data = {
            'name': 'Updated Product',
            'price': 15,
            'img': 'updated.jpg',
            'description': 'Updated description',
            'category': Product.Category.STARTER,
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Product')

    def test_delete_product(self):
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )
        url = reverse('product-detail', args=[product.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product.id).exists())

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'number': 1,
            'table_id': 1,
            'customer_id': 1,
            'state': Order.State.ORDERING,
            'total_check': 0,
            'percentage_tip': 0,
            'total_tip': 0,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data['id'])
        self.assertEqual(order.number, 1)

    def test_retrieve_order(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        url = reverse('order-detail', args=[order.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], 1)

    def test_update_order(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        url = reverse('order-detail', args=[order.id])
        data = {
            'number': 2,
            'table_id': 2,
            'customer_id': 2,
            'state': Order.State.CHECKING,
            'total_check': 100,
            'percentage_tip': 10,
            'total_tip': 10,
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.number, 2)

    def test_delete_order(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        url = reverse('order-detail', args=[order.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=order.id).exists())

class QuantityTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_quantity(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )

        url = reverse('quantity-list')
        data = {
            'order': order.id,
            'product': product.id,
            'quantity': 1,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quantity = Quantity.objects.get(pk=response.data['id'])
        self.assertEqual(quantity.order, order)
        self.assertEqual(quantity.product, product)
        self.assertEqual(quantity.quantity, 1)

    def test_retrieve_quantity(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )
        quantity = Quantity.objects.create(
            order=order,
            product=product,
            quantity=1,
        )
        url = reverse('quantity-detail', args=[quantity.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 1)

    def test_update_quantity(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )
        quantity = Quantity.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        url = reverse('quantity-detail', args=[quantity.id])
        data = {
            'quantity': 2,
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quantity.refresh_from_db()
        self.assertEqual(quantity.quantity, 2)

    def test_delete_quantity(self):
        order = Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=0,
            percentage_tip=0,
            total_tip=0,
        )
        product = Product.objects.create(
            name='Test Product',
            price=10,
            img='test.jpg',
            description='Test description',
            category=Product.Category.MAIN,
        )
        quantity = Quantity.objects.create(
            order=order,
            product=product,
            quantity=1,
        )
        url = reverse('quantity-detail', args=[quantity.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Quantity.objects.filter(pk=quantity.id).exists())

class OrderFilterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_order_filter_view(self):
        Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.ORDERING,
            total_check=100,
            percentage_tip=10,
            total_tip=10,
            date_created=datetime.now(),
            date_paid=datetime.now(),
        )
        Order.objects.create(
            number=2,
            table_id=2,
            customer_id=2,
            state=Order.State.ORDERING,
            total_check=200,
            percentage_tip=20,
            total_tip=20,
            date_created=datetime.now(),
            date_paid=datetime.now(),
        )

        url = reverse('order-filter')
        data = {
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrderDeleteViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_order_delete_view(self):
        Order.objects.create(
            number=1,
            table_id=1,
            customer_id=1,
            state=Order.State.PAID,
            total_check=100,
            percentage_tip=10,
            total_tip=10,
            date_created=datetime.now(),
            date_paid=datetime.now(),
        )
        Order.objects.create(
            number=2,
            table_id=2,
            customer_id=2,
            state=Order.State.PAID,
            total_check=200,
            percentage_tip=20,
            total_tip=20,
            date_created=datetime.now(),
            date_paid=datetime.now(),
        )

        url = reverse('order-delete')
        data = {
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

