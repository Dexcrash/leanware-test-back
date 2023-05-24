import json
from datetime import date
from django.test import TestCase
from django.db.models import Sum
from rest_framework import status
from rest_framework.test import APIClient
from faker import Faker
from .models import Product, Order
from .serilizers import ProductSerializer, OrderSerializer
from .factories import ProductFactory, OrderFactory
import logging

# Get the logger for the current module
logger = logging.getLogger(__name__)

fake = Faker()


class OrderViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_order_list(self):
        products = ProductFactory.create_batch(2)
        orders = OrderFactory.create_batch(2)
        for order in orders:
            order.products.set(products)

        url = '/api/orders/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        serialized_orders = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serialized_orders.data)


    def test_get_order_detail(self):
        order = OrderFactory()

        url = f'/api/orders/{order.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, OrderSerializer(order).data)

    def test_create_order(self):
        product1 = ProductFactory()
        product2 = ProductFactory()

        url = '/api/orders/'
        data = {
            'number': fake.random_int(min=1, max=100),
            'total_check': fake.random_int(min=10, max=100),
            'total_tip': fake.random_int(min=1, max=10),
            'date_created': fake.date(),
            'products': [product1.id, product2.id]
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['number'], data['number'])
        self.assertEqual(response.data['total_check'], data['total_check'])
        self.assertEqual(response.data['total_tip'], data['total_tip'])
        self.assertEqual(response.data['products'], data['products'])

    def test_update_order(self):
        order = OrderFactory()
        product = ProductFactory()

        url = f'/api/orders/{order.id}/'
        data = {
            'number': fake.random_int(min=1, max=100),
            'total_check': fake.random_int(min=10, max=100),
            'total_tip': fake.random_int(min=1, max=10),
            'date_created': fake.date(),
            'products': [product.id]
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['number'], data['number'])
        self.assertEqual(response.data['total_check'], data['total_check'])
        self.assertEqual(response.data['total_tip'], data['total_tip'])
        self.assertEqual(response.data['products'], data['products'])

    def test_delete_order(self):
        order = OrderFactory()

        url = f'/api/orders/{order.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=order.id).exists())

class ProductViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_product_list(self):
        products = ProductFactory.create_batch(2)

        url = '/api/products/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        serialized_products = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serialized_products.data)

    def test_get_product_detail(self):
        product = ProductFactory()

        url = f'/api/products/{product.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ProductSerializer(product).data)

    def test_create_product(self):
        url = '/api/products/'
        data = {
            'name': fake.name(),
            'price': fake.random_int(min=1, max=100),
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['price'], data['price'])

    def test_update_product(self):
        product = ProductFactory()

        url = f'/api/products/{product.id}/'
        data = {
            'name': fake.name(),
            'price': fake.random_int(min=1, max=100),
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['price'], data['price'])

    def test_delete_product(self):
        product = ProductFactory()

        url = f'/api/products/{product.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=product.id).exists())

class OrderDeleteViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_delete_orders(self):
        # Create orders with specific dates
        order1 = OrderFactory.create(date_created=date(2023, 1, 1), date_paid=date(2023, 1, 2))
        order2 = OrderFactory.create(date_created=date(2023, 6, 1), date_paid=date(2023, 6, 2))
        order3 = OrderFactory.create(date_created=date(2024, 1, 1), date_paid=None)

        url = '/api/delete/'
        start_date = '2023-01-01'
        end_date = '2023-12-31'

        response = self.client.post(url, data={'start_date': start_date, 'end_date': end_date})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['orders_deleted'], 2)
        self.assertFalse(Order.objects.filter(id=order1.id).exists())
        self.assertFalse(Order.objects.filter(id=order2.id).exists())
        self.assertTrue(Order.objects.filter(id=order3.id).exists())

        # Verify that the order in progress (order3) was not deleted

    def test_delete_orders_invalid_dates(self):
        url = '/api/delete/'
        response = self.client.post(url, data={'start_date': 'invalid', 'end_date': 'date'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid date format. Please provide dates in the format: YYYY-MM-DD.')

    def test_delete_orders_missing_dates(self):
        url = '/api/delete/'
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'start_date and end_date are required.')

class OrderFilterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_filter_orders(self):
        # Create orders with specific dates
        order1 = OrderFactory.create(date_created=date(2023, 1, 1))
        order2 = OrderFactory.create(date_created=date(2023, 6, 1))
        order3 = OrderFactory.create(date_created=date(2024, 1, 1))

        url = '/api/filter/'
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)
        data={'start_date': start_date, 'end_date': end_date}

        response = self.client.post(url, data={'start_date': start_date, 'end_date': end_date})

        # Calculate the expected total check and total tip based on the filtered orders
        filtered_orders = [order for order in [order1, order2, order3] if start_date <= order.date_created <= end_date]
        total_check = sum(order.total_check for order in filtered_orders)
        total_tip = sum(order.total_tip for order in filtered_orders)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['orders'], OrderSerializer(filtered_orders, many=True).data)
        self.assertEqual(response.data['total_check'], total_check)
        self.assertEqual(response.data['total_tip'], total_tip)

    def test_filter_orders_invalid_dates(self):
        url = '/api/filter/'
        data={'start_date': 'invalid', 'end_date': 'date'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid date format. Please provide dates in the format: YYYY-MM-DD.')

    def test_filter_orders_missing_dates(self):
        url = '/api/filter/'
        data={}
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'start_date and end_date are required.')
