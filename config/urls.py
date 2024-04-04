from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="API Title",
      default_version='v1',
      description="API Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += [
    # admin
    path('admin/', admin.site.urls),
    # local urls
    # path('account/', include('apps.account.api.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('product/', include('apps.product.urls')),
    path('blog/', include('apps.blog.urls')),
    # path('order/', include('apps.order.api.urls')),

    # path('order/', include('apps.order.api.urls')),
]


@api_view(['GET'])
@permission_classes([AllowAny])
def swagger_view(request):
    return schema_view.with_ui('swagger', cache_timeout=0)(request)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




