from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, QuanityViewSet, OrderFilterView, OrderDeleteView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'quantity', QuanityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/filter/', OrderFilterView.as_view(), name='order-filter'),
    path('api/delete/', OrderDeleteView.as_view(), name='order-delete'),
]
