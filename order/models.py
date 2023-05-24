from django.db import models
from django.db.models import UniqueConstraint

class Product(models.Model):
    class Category(models.TextChoices):
        STARTER = "1", "STARTER"
        MAIN = "2", "MAIN COURSE"
        DESSERT = "3", "DESSERT"

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    img = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.MAIN
    )

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    class State(models.TextChoices):
        ORDERING = "1", "ORDERING"
        CHECKING = "2", "CHECKING"
        PAID = "3", "PAID"

    number = models.IntegerField()
    table_id = models.IntegerField()
    customer_id = models.IntegerField()
    waiter_id = models.IntegerField(default=1)
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.ORDERING
    )
    total_check = models.IntegerField(default=0)
    percentage_tip = models.IntegerField(default=0)
    total_tip = models.IntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)
    date_paid = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['table_id', 'customer_id'],
                condition=models.Q(state='1'),  # Only for state '1' (ORDERING)
                name='unique_order_table_customer'
            )
        ]

    def __str__(self):
        return str(self.number)
    
class Quantity(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.quantity)