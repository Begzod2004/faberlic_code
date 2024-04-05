from django.urls import include, path
from rest_framework import routers
from .views import  CategoryViewSet, RecCategoryViewSet, GetFilterProductViewSet, ProductRatingViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'product-filterGet', GetFilterProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'product-ratings', ProductRatingViewSet)
router.register(r'reccategory', RecCategoryViewSet)
router.register(r'orders', OrderViewSet) 



urlpatterns = [
    path('', include(router.urls))
]
