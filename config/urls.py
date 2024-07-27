from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

from config.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

urlpatterns = [
    path("api/", include("apps.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": MEDIA_ROOT,
        },
    ),
]
