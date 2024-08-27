import os

import requests
from django.db import transaction
from django.db.models import Max, Min
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from requests import Request
from rest_framework import mixins, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from dotenv import load_dotenv
load_dotenv()

from apps.product.models import (Banner, Category, 
                                 IndexCategory, Order, OrderUser,
                                 ShortDescription, Stock, SubCategory)
from apps.product.serializers import (AllCategorySerializer, BannerSerializer,
                                      CategoryCountSerializer,
                                      CategorySerializer,
                                      ImageModelSerializer,
                                      IndexCategorySerializer,
                                      MainPageCategorySerializer,
                                      OrderUserGetSerializer,
                                      ProductCatalogSerializer,
                                      ProductSearchSerializer,
                                      ProductSerializer,
                                      OrderUserAnalyticsSerializer,
                                      ShortDescriptionSerializer,
                                      StockSerializer, SubCategorySerializer)
from config.settings import MEDIA_ROOT

from .filters import ProductFilter, ProductSearchFilter, OrderUserFilter
from .models import Images, Product
from .pagination import CustomPagination
from .serializers import OrderUserSerializer


class SearchListApiView(ListAPIView):
    serializer_class = ProductSearchSerializer
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductSearchFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает продукты в порядке убывания ID с изображениями и необходимыми полями.
        """
        queryset = Product.objects.all().order_by("-id")

        queryset = queryset.select_related(
            "stock", "sub_category", "category"
        ).prefetch_related("images")

        return queryset




# Image API
class ImageListCreateView(ListCreateAPIView):
    queryset = Images.objects.all().order_by("-id")
    serializer_class = ImageModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["image"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["image"])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            created_images = serializer.save()

            image_data = [
                {"id": image.id, "url": request.build_absolute_uri(image.image.url)}
                for image in created_images
            ]

            response_data = {"images": image_data}
            return Response(response_data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ImageRetrieveView(RetrieveAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageModelSerializer

    @extend_schema(tags=["image"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ImageUpdateView(UpdateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageModelSerializer
    lookup_field = "id"

    @extend_schema(tags=["image"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["image"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class DeleteImages(APIView):
    serializer_class = ImageModelSerializer

    @staticmethod
    @extend_schema(tags=["image"])
    def delete(request):
        image_ids = request.data.get("image_ids", [])

        if not image_ids:
            return Response(
                {"detail": "Please provide image_ids to delete."},
                status=HTTP_400_BAD_REQUEST,
            )

        images = Images.objects.filter(pk__in=image_ids)
        deleted_image_data = []

        for image in images:
            image_url = request.build_absolute_uri(image.image.url)
            image_path = os.path.join(MEDIA_ROOT, str(image.image))

            if os.path.exists(image_path):
                os.remove(image_path)

            deleted_image_data.append({"id": image.id, "url": image_url})

        num_deleted, _ = images.delete()

        if num_deleted > 0:
            return Response({"images_deleted": deleted_image_data}, status=HTTP_200_OK)
        else:
            return Response(
                {"detail": "No images were deleted."}, status=HTTP_400_BAD_REQUEST
            )


class CategoryCountAPIView(APIView):
    serializer_class = CategoryCountSerializer

    @extend_schema(tags=["category"])
    def get(self, request, *args, **kwargs):
        count = Category.objects.filter(is_index=True).count()
        data = {"count": count}
        serializer = CategoryCountSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)



class AllCategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AllCategorySerializer
    queryset = Category.objects.none()

    @extend_schema(
        tags=["category"],
        operation_id="listAllCategories",
    )
    def list(self, request, *args, **kwargs):
        all_categories = Category.objects.all()

        # Initialize min and max prices for all categories
        min_price_all = float("inf")
        max_price_all = float("-inf")

        category_data = []  # To store serialized category data

        for category in all_categories:
            # Calculate min and max prices for the current category
            min_price_category = (
                category.sub_categories.aggregate(Min("products__price"))[
                    "products__price__min"
                ]
                or 0.0
            )
            max_price_category = (
                category.sub_categories.aggregate(Max("products__price"))[
                    "products__price__max"
                ]
                or 0.0
            )

            # Update overall min and max prices
            min_price_all = min(min_price_all, min_price_category)
            max_price_all = max(max_price_all, max_price_category)

            # Serialize the category
            serializer = AllCategorySerializer(
                category, context={"request": self.request}
            )
            category_data.append(serializer.data)  # Add serialized data to list

        # Build the response data
        data = {
            "categories": category_data,
            "min_price_all": min_price_all,
            "max_price_all": max_price_all,
        }

        return Response(data, status=status.HTTP_200_OK)


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["category"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "id"

    @extend_schema(tags=["category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["category"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["category"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["category"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class MainPageCategoryView(ListAPIView):
    queryset = Category.objects.filter(is_index=True).order_by("-id")[:9]
    serializer_class = MainPageCategorySerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class StockListCreateView(ListCreateAPIView):
    queryset = Stock.objects.all().order_by("-id")
    serializer_class = StockSerializer

    @extend_schema(tags=["stock"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["stock"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StockDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    lookup_field = "id"
    serializer_class = StockSerializer

    @extend_schema(tags=["stock"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["stock"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["stock"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["stock"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubCategoryListCreateView(ListCreateAPIView):
    queryset = SubCategory.objects.all().order_by("-id")
    serializer_class = SubCategorySerializer

    @extend_schema(tags=["sub-category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["sub-category"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubCategoryDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    lookup_field = "id"
    serializer_class = SubCategorySerializer

    @extend_schema(tags=["sub-category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["sub-category"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["sub-category"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["sub-category"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



class IndexCategoryListCreateView(ListCreateAPIView):
    queryset = IndexCategory.objects.all().order_by("-id")
    serializer_class = IndexCategorySerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["index-category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["index-category"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class IndexCategoryDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = IndexCategory.objects.all()
    serializer_class = IndexCategorySerializer
    lookup_field = "id"
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["index-category"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["index-category"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["index-category"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["index-category"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer

    @extend_schema(tags=["products"])
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_queryset(), context={"request": request}, many=True
        )
        return Response(serializer.data)

    @extend_schema(tags=["products"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class ProductCatalogView(ListAPIView):
    serializer_class = ProductCatalogSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ("price", "title_ru", "title_uz")
    pagination_class = CustomPagination

    def get_queryset(self):
        ordering = self.request.query_params.get("ordering", "-id")

        # Очистка параметра сортировки для проверки его корректности

        if ordering not in self.ordering_fields:
            ordering = "-id"

        queryset = Product.objects.all().order_by(ordering)

        # Использовать select_related для загрузки связанных объектов одним запросом

        queryset = queryset.select_related("stock", "sub_category", "category")

        # Использовать prefetch_related для оптимизации многих-ко-многим и обратных связей

        queryset = queryset.prefetch_related("images")

        return queryset

    @extend_schema(tags=["catalog-product"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)




class ProductDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related("stock", "sub_category", "category")
    serializer_class = ProductSerializer
    lookup_field = "slug"

    @extend_schema(tags=["products"])
    def get(self, request, *args, **kwargs):
        # Обрабатывает GET-запросы для получения деталей продукта.
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["products"])
    def put(self, request, *args, **kwargs):
        # Обрабатывает PUT-запросы для обновления продукта.
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["products"])
    def patch(self, request, *args, **kwargs):
        # Обрабатывает PATCH-запросы для частичного обновления продукта.
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["products"])
    def delete(self, request, *args, **kwargs):
        # Обрабатывает DELETE-запросы для удаления продукта.
        return super().delete(request, *args, **kwargs)



class ShortDescriptionListCreateView(ListCreateAPIView):
    queryset = ShortDescription.objects.all().order_by("-id")
    serializer_class = ShortDescriptionSerializer

    @extend_schema(tags=["short-description"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["short-description"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ShortDescriptionDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ShortDescription.objects.all()
    serializer_class = ShortDescriptionSerializer
    lookup_field = "id"

    @extend_schema(tags=["short-description"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["short-description"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["short-description"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["short-description"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AdvertisementBannerListView(ListAPIView):
    queryset = Banner.objects.filter(is_advertisement=True).order_by("-id")
    serializer_class = BannerSerializer

    @extend_schema(tags=["banner"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BannerListCreateView(ListCreateAPIView):
    queryset = Banner.objects.filter(is_advertisement=False).order_by("-id")
    serializer_class = BannerSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["banner"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["banner"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        banner_instance = serializer.save()

        # Handle images for the banner
        web_image = request.data.get("web_image")
        rsp_image = request.data.get("rsp_image")

        if web_image:
            banner_instance.web_image = web_image
        if rsp_image:
            banner_instance.rsp_image = rsp_image

        banner_instance.save()

        response_data = serializer.data

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = serializer.save()
        images_serializer = BannerSerializer(instance)
        serializer.data["web_image"] = images_serializer.data["web_image"]
        serializer.data["rsp_image"] = images_serializer.data["rsp_image"]



class BannerDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    lookup_field = "id"
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["banner"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    @extend_schema(tags=["banner"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["banner"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["banner"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class BannerListView(ListAPIView):
    queryset = Banner.objects.order_by("-id")
    serializer_class = BannerSerializer

    @extend_schema(tags=["banner"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class SubmitOrderView(CreateAPIView):
    serializer_class = OrderUserSerializer

    @transaction.atomic
    @extend_schema(tags=["orders"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_items = serializer.validated_data.get("order", [])
        order_text, total_price = self._process_order_items(order_items)

        order_user = serializer.save(total_price=total_price)
        if order_user:
            self._send_order_notification(order_user, order_text, total_price)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _process_order_items(self, order_items):
        order_text = ""
        total_price = 0

        for index, item in enumerate(order_items, start=1):
            product, product_count = self._get_product_and_count(item)
            product_price = product.sales or product.price
            product_total_price = product_count * product_price

            total_price += product_total_price
            order_text += self._format_product_detail(
                index, product, product_count, product_price
            )

        return order_text, total_price

    def _get_product_and_count(self, item):
        product_or_id = item.get("product_id", 0)
        product_count = item.get("count", 0)

        if isinstance(product_or_id, Product):
            product = product_or_id
        else:
            try:
                product = Product.objects.get(id=product_or_id)
            except Product.DoesNotExist:
                raise Http404(f"Product with ID {product_or_id} not found")

        return product, product_count

    def _format_product_detail(self, index, product, count, price):
        return (
            f"➊ {index}) <b>Mahsulot:</b> {product.title_uz}\n"
            f"    <b>Soni:</b> {count} dona\n"
            f"    <b>Narxi:</b> {price} so'm\n\n"
        )

    def _send_order_notification(self, order_user, order_text, total_price):
        name = order_user.name or "Noma'lum"
        phone = order_user.phone or "Noma'lum"
        address = order_user.address or "Noma'lum"
        text = (
            f"<b>📦 Yangi Zakaz!</b> 📦\n\n"
            f"<b>👤 Ism:</b> {name}\n\n"
            f"<b>📞 Telefon:</b> {phone}\n\n"
            f"<b>🏠 Manzil:</b> {address}\n\n"
            f"<b>🛒 Mahsulotlar:</b>\n\n"
            f"{order_text}"
            f"<b>💰 Jami narx:</b> {total_price} so'm"
        )

        token = os.environ.get("BOT_TOKEN")
        if not token:
            print("BOT_TOKEN environment variable is not set.")
            return

        # user_ids = ["1237819772",]
        user_ids = os.environ.get("USER_IDS", "").split(" ")
        if not user_ids:
            raise ValueError("USER_IDS environment variable is not set")

        for user_id in user_ids:
            response = self._send_telegram_message(token, user_id, text)


    @staticmethod
    def _send_telegram_message(token, user_id, text):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": text,
            "parse_mode": "HTML",
        }
        try:
            response = requests.post(
                url, json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")



# optimizied version

# added filter


class OrderListView(ListAPIView):
    serializer_class = OrderUserGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderUserFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает queryset объектов OrderUser, упорядоченных по дате создания,
        с предварительной загрузкой связанных объектов Order.
        """
        return OrderUser.objects.prefetch_related("user_orders").order_by("-created_at")

    @extend_schema(tags=["orders"])
    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запросы для получения постраничного и отфильтрованного списка заказов.
        """
        return super().get(request, *args, **kwargs)


class OrderUserAnalyticsView(RetrieveAPIView):
    serializer_class = OrderUserAnalyticsSerializer

    # permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["order-analytics"],
        parameters=[
            OpenApiParameter(
                name="phone",
                description="Phone number of the user",
                required=True,
                type=str,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")
        if not phone:
            return Response({"detail": "Phone number is required"}, status=400)

        try:
            order_user = OrderUser.objects.filter(phone=phone).latest("created_at")
        except OrderUser.DoesNotExist:
            return Response(
                {"detail": "OrderUser with this phone number does not exist"},
                status=404,
            )
        except OrderUser.MultipleObjectsReturned:
            order_user = OrderUser.objects.filter(phone=phone).latest("created_at")

        serializer = self.get_serializer(order_user)
        return Response(serializer.data)
