from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated  
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Category, RecCategory, Product, ProductRating, Order
from .serializers import (
    CategorySerializer,
    RecCategorySerializer,
    GetProductSerializer,
    ProductRatingSerializer,
    OrderSerializer,
) 
from .filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'head', 'options']

class RecCategoryViewSet(viewsets.ModelViewSet):
    queryset = RecCategory.objects.all()
    serializer_class = RecCategorySerializer

class GetFilterProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    parser_classes = (FormParser, MultiPartParser) 
    serializer_class = GetProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Add DjangoFilterBackend
    search_fields = ['translations__name', 'translations__description']  # Expand  
    ordering_fields = ['created_at', 'name', 'type_product']

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all().order_by(F('star').desc())
    serializer_class = ProductRatingSerializer

from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):  # Use ModelViewSet for full CRUD
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        """Filters orders to show only those belonging to the current user."""
        return self.queryset.filter(user=self.request.user) 
