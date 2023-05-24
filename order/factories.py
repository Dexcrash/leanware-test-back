import factory
from faker import Faker
from order.models import Product, Order

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    price = factory.LazyFunction(lambda: fake.random_int(min=10, max=100))

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    number = factory.Sequence(lambda n: n)
    total_check = factory.LazyFunction(lambda: fake.random_int(min=10, max=100))
    total_tip = factory.LazyFunction(lambda: fake.random_int(min=1, max=10))
    date_created = factory.LazyFunction(fake.date)
    date_paid = factory.LazyFunction(fake.date)
