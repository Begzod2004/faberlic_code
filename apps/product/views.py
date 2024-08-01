import os

import requests
from django.db import transaction
from django.db.models import Max, Min
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
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

from apps.product.models import (Banner, Brand, Category, 
                                 IndexCategory, Order, OrderUser,
                                 ShortDescription, Stock, SubCategory)
from apps.product.serializers import (AllCategorySerializer, BannerSerializer,
                                      BrandSerializer, CategoryCountSerializer,
                                      CategorySerializer,
                                      ImageModelSerializer,
                                      IndexCategorySerializer,
                                      MainPageCategorySerializer,
                                      OrderUserGetSerializer,
                                      ProductCatalogSerializer,
                                      ProductSearchSerializer,
                                      ProductSerializer,
                                      ShortDescriptionSerializer,
                                      StockSerializer, SubCategorySerializer)
from config.settings import MEDIA_ROOT

from .filters import ProductFilter, ProductSearchFilter
from .models import Images, Product
from .pagination import CustomPagination
from .serializers import OrderUserSerializer


class SearchListApiView(ListAPIView):
    queryset = Product.objects.all().order_by("-id")
    renderer_classes = [JSONRenderer]
    serializer_class = ProductSearchSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = ProductSearchFilter
    search_fields = ("title_uz", "title_ru")
    pagination_class = CustomPagination

    @extend_schema(tags=["catalog-search"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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

        all_brands = Brand.objects.all()
        brand_info = []
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

            # Use self.request directly in the serializer's context
            serializer = AllCategorySerializer(
                category, context={"request": self.request}
            )

            # Add category data to the response
            brand_info.append(
                {
                    "id": category.id,
                    "title_uz": category.title_uz,
                    "title_ru": category.title_ru,
                    "image": serializer.data["image"],
                    "min_price": min_price_category,
                    "max_price": max_price_category,
                    "brands": serializer.data["brands"],
                    "sub_categories": serializer.data["sub_categories"],
                }
            )

        # Build the response data
        data = {
            "min_price": min_price_all,
            "max_price": max_price_all,
            "all_catalog": brand_info,
            "brands": BrandSerializer(all_brands, many=True).data,
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


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all().order_by("-id")
    serializer_class = BrandSerializer

    @extend_schema(tags=["brands"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["brands"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BrandDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "id"

    @extend_schema(tags=["brands"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["brands"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["brands"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["brands"])
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
    queryset = Product.objects.all().order_by("-id")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ("price", "title_ru", "title_uz")
    pagination_class = CustomPagination

    @extend_schema(tags=["catalog-product"])
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all().order_by("pk")
        return self.list(request, *args, queryset=queryset, **kwargs)


class ProductDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    @extend_schema(tags=["products"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["products"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["products"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["products"])
    def delete(self, request, *args, **kwargs):
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

    # @extend_schema(tags=["banner"])
    # def put(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     # Extract and process the stock field from the request data
    #     stock_name = request.data.get("stock")
    #     print("Stock name from request:", stock_name)
    #
    #     if stock_name:
    #         stock = get_object_or_404(Stock, title=stock_name)
    #         instance.stock = stock
    #         instance.save()  # Save the instance with the updated stock
    #         print("Stock from request:", stock)
    #
    #     # Create the serializer instance with the modified request data
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # Handle images for the banner
    #     web_image = request.data.get("web_image")
    #     rsp_image = request.data.get("rsp_image")
    #
    #     if web_image:
    #         instance.web_image = web_image
    #     if rsp_image:
    #         instance.rsp_image = rsp_image
    #
    #     # Save the instance with the updated serializer
    #     serializer.save()
    #
    #     response_data = serializer.data
    #
    #     return Response(response_data)

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


# class SubmitOrderView(CreateAPIView):
#     serializer_class = OrderUserSerializer
#
#     @transaction.atomic
#     @extend_schema(tags=["orders"])
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             order_items = serializer.validated_data.get("order", [])
#             total_price = 0
#             order_text = ""
#             product_ids_in_order = set()
#
#             for item in order_items:
#                 product_id = item.get("product_id", 0)
#                 product_count = item.get("count", 0)
#
#                 try:
#                     product = item.get("product_id")
#                     product_id = product.id if product else None
#                 except Product.DoesNotExist:
#                     raise Http404(f"Product with ID {product_id} not found")
#
#                 product_price = product.sales if product.sales else product.price
#
#                 product_total_price = product_count * product_price
#                 total_price += product_total_price
#
#                 product_detail = f"🔹 Tovar: {product.title_uz}\n🔸 Soni: {product_count}\n🔸 Narxi: {product_price}\n"
#                 order_text += product_detail
#
#                 if product_id not in product_ids_in_order:
#                     product_ids_in_order.add(product_id)
#
#             order_user = serializer.save(total_price=total_price)
#
#             name = order_user.name
#             phone = order_user.phone
#             address = order_user.address
#
#             text = f"\n\n\n\n\n📦 Yangi zakaz tushdi 📦\n\n"
#             text += f"👤 Ism: {name}\n📞 Telefon Nomer: {phone}\n🏠 Manzil: {address}\n"
#             text += "\n\n🛒 Zakaz qilingan tovarlar: \n\n"
#             text += order_text
#             text += f"\n💰 Umumiy narxi: {total_price}"
#
#             token = os.environ.get("BOT_TOKEN")
#             user_ids = ["1237819772", "95665294"]
#
#             for user_id in user_ids:
#                 url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={text}"
#                 print(requests.get(url))
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmitOrderView(CreateAPIView):
    serializer_class = OrderUserSerializer

    @transaction.atomic
    @extend_schema(tags=["orders"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_items = serializer.validated_data.get("order", [])
            total_price = 0
            order_text = ""
            product_ids_in_order = set()

            # Declare order_user variable here
            order_user = None

            for item in order_items:
                product_id = item.get("product_id", 0)
                product_count = item.get("count", 0)

                try:
                    product = item.get("product_id")
                    if isinstance(
                        product, Product
                    ):  # Check if it's already a Product object
                        product_id = product.id
                        product_title = product.title_uz
                    else:
                        product = Product.objects.get(id=product_id)
                        product_title = product.title_uz
                except Product.DoesNotExist:
                    raise Http404(f"Product with ID {product_id} not found")

                product_price = product.sales if product.sales else product.price

                product_total_price = product_count * product_price
                total_price += product_total_price

                product_detail = f"🔹 Tovar: {product_title}\n🔸 Soni: {product_count}\n🔸 Narxi: {product_price}\n"
                order_text += product_detail

                if product_id not in product_ids_in_order:
                    product_ids_in_order.add(product_id)

                # Save the order with product_title
                if order_user is None:
                    order_user = serializer.save(
                        total_price=total_price, product_title=product_title
                    )

                Order.objects.create(
                    product_id=product,
                    product_title=product_title,
                    count=product_count,
                    order=order_user,
                )

            name = order_user.name
            phone = order_user.phone
            address = order_user.address

            text = f"\n\n\n\n\n📦 Yangi zakaz tushdi 📦\n\n"
            text += f"👤 Ism: {name}\n📞 Telefon Nomer: {phone}\n🏠 Manzil: {address}\n"
            text += "\n\n🛒 Zakaz qilingan tovarlar: \n\n"
            text += order_text
            text += f"\n💰 Umumiy narxi: {total_price}"

            token = os.environ.get("BOT_TOKEN")
            user_ids = ["1237819772"]

            for user_id in user_ids:
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={text}"
                print(requests.get(url))

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(ListAPIView):
    queryset = OrderUser.objects.order_by("-created_at")
    serializer_class = OrderUserGetSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["orders"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
