from rest_framework import viewsets, filters
from .serializers import  ProductSerializer, SubCategorySerializer, GetProductSerializer, ProductRatingSerializer
from .models import Product, SubCategory, ProductRating
from .filters import ProductFilter
from rest_framework.filters import SearchFilter
from .models import Category
from rest_framework import viewsets
from django.db.models import F
from .serializers import CategorySerializer
from .filters import ProductFilter  # Filterni import qiling
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'head', 'options']

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class GetFilterProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['translations__name']      #'translations__description'
    ordering_fields = ['created_at', 'name', 'type_product']

    def get_queryset(self):
        # Get the search query from the request
        search_query = self.request.GET.get('search', '')

        # Perform the search and select related company data
        queryset = Product.objects.filter(translations__name__icontains=search_query).select_related('company')

        return queryset

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all().order_by(F('star').desc())
    serializer_class = ProductRatingSerializer






