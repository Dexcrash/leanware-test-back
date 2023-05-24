from rest_framework import serializers
from .models import Product, Order, Quantity

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = '__all__'