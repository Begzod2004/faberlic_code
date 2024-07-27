from django.urls import include, path

urlpatterns = [
    path("", include("apps.product.urls")),
    path("about/", include("apps.about.urls")),
    path("users/", include("apps.users.urls")),
]
