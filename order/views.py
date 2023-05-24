from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Sum
from datetime import datetime
from .models import Product, Order, Quantity
from .serilizers import ProductSerializer, OrderSerializer, QuantitySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class QuanityViewSet(ModelViewSet):
    queryset = Quantity.objects.all()
    serializer_class = QuantitySerializer

class OrderFilterView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Perform input validation
        if not start_date or not end_date:
            return Response({'error': 'start_date and end_date are required.'}, status=400)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Please provide dates in the format: YYYY-MM-DD.'}, status=400)
        
        orders = Order.objects.filter(date_created__range=[start_date, end_date])
        total_check = orders.aggregate(total_check=Sum('total_check'))['total_check']
        total_tip = orders.aggregate(total_tip=Sum('total_tip'))['total_tip']
        
        serializer = OrderSerializer(orders, many=True)
        data = {
            'orders': serializer.data,
            'total_check': total_check,
            'total_tip': total_tip
        }
        
        return Response(data)
    
class OrderDeletionService:
    @staticmethod
    def delete_orders(start_date, end_date):
        orders = Order.objects.filter(date_created__range=[start_date, end_date], state="3")
        orders_deleted, _ = orders.delete()
        return orders_deleted

class OrderDeleteView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Perform input validation
        if not start_date or not end_date:
            return Response({'error': 'start_date and end_date are required.'}, status=400)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Please provide dates in the format: YYYY-MM-DD.'}, status=400)

        # Call the OrderDeletionService to delete the orders
        orders_deleted = OrderDeletionService.delete_orders(start_date, end_date)

        return Response({'orders_deleted': orders_deleted})

