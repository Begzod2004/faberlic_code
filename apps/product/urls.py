from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.product import views
from apps.product.views import (AllCategoryViewSet, ProductCatalogView,
                                SearchListApiView)

router = DefaultRouter()

# Register the viewset with the router
router.register(r"all-categories", AllCategoryViewSet, basename="all-categories")
urlpatterns = [
    path("images/", views.ImageListCreateView.as_view(), name="image-list-create"),
    path("images/<int:pk>/", views.ImageRetrieveView.as_view(), name="image-retrieve"),
    path(
        "images/update/<int:pk>/", views.ImageUpdateView.as_view(), name="image-update"
    ),
    path(
        "images/delete/",
        views.DeleteImages.as_view(),
        name="delete-multiple-images",
    ),
    path(
        "categories/",
        views.CategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:id>/",
        views.CategoryDetailUpdateDestroyView.as_view(),
        name="category-retrieve-update-destroy",
    ),
    path(
        "categories-count/", views.CategoryCountAPIView.as_view(), name="category-count"
    ),
    path(
        "sub_categories/",
        views.SubCategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "sub_categories/<int:id>/",
        views.SubCategoryDetailUpdateDestroyView.as_view(),
        name="category-retrieve-update-destroy",
    ),
    path(
        "brands/",
        views.BrandListCreateView.as_view(),
        name="brand-list-create",
    ),
    path(
        "brands/<int:id>/",
        views.BrandDetailUpdateDestroyView.as_view(),
        name="brand-retrieve-update-destroy",
    ),
    path(
        "products/",
        views.ProductListCreateView.as_view(),
        name="products-list-create",
    ),
    path(
        "products/<slug:slug>/",
        views.ProductDetailUpdateDestroyView.as_view(),
        name="product-retrieve-update-destroy",
    ),
    path("products-catalog", ProductCatalogView.as_view(), name="product-catalog"),
    path(
        "short-description/",
        views.ShortDescriptionListCreateView.as_view(),
        name="short-description-list-create",
    ),
    path(
        "short-description/<int:id>/",
        views.ShortDescriptionDetailUpdateDestroyView.as_view(),
        name="short-description-retrieve-update-destroy",
    ),

    path("product-search", SearchListApiView.as_view(), name="catalog-search"),
    path(
        "banners/",
        views.BannerListCreateView.as_view(),
        name="banners-list-create",
    ),
    path(
        "banner/",
        views.BannerListView.as_view(),
        name="banners-list",
    ),
    path(
        "banners/<int:id>/",
        views.BannerDetailUpdateDestroyView.as_view(),
        name="banners-retrieve-update-destroy",
    ),
    path(
        "ad-banners/",
        views.AdvertisementBannerListView.as_view(),
        name="advertisement-banner-list",
    ),
    path("categories/", include(router.urls)),
    path("product-orders/", views.SubmitOrderView.as_view(), name="product-order"),
    path("order-list", views.OrderListView.as_view(), name="order-list"),
    path(
        "index-categories/",
        views.IndexCategoryListCreateView.as_view(),
        name="index-categories-list-create",
    ),
    path(
        "index-categories/<int:id>/",
        views.IndexCategoryDetailUpdateDestroyView.as_view(),
        name="index-categories-retrieve-update-destroy",
    ),
    path(
        "main-page-categories/",
        views.MainPageCategoryView.as_view(),
        name="main-page-categories",
    ),
    path(
        "stocks/",
        views.StockListCreateView.as_view(),
        name="stock-list-create",
    ),
    path(
        "stocks/<int:id>/",
        views.StockDetailUpdateDestroyView.as_view(),
        name="stock-retrieve-update-destroy",
    ),
]
