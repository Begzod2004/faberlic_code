from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.product'

    def ready(self):
        import apps.product.translation  # Bu qismni qo'shib ko'ring