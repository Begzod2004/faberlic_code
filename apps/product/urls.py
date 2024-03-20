from django.urls import include, path
from rest_framework import routers
from .views import  CategoryViewSet, SubCategoryViewSet, GetFilterProductViewSet, ProductRatingViewSet

router = routers.DefaultRouter()
router.register(r'product-filterGet', GetFilterProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'product-ratings', ProductRatingViewSet)
router.register(r'subcategory', SubCategoryViewSet)


urlpatterns = [
    path('', include(router.urls))
]
