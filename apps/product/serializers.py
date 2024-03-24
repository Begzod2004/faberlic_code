from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import  Product, Category, RecCategory, ProductImage, ProductRating
from rest_framework import serializers
from django.db.models import Avg


class RecCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=RecCategory)
    
    class Meta:
        model = RecCategory
        fields = '__all__'


class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer'

    def get_reccategory(self, category_instance):
        reccategories = RecCategory.objects.filter(category=category_instance)
        serializer = RecCategorySerializer(reccategories, many=True)
        return serializer.data
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
    
    
class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category = RecCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'



class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class ProductRetrieveSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    product_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    category = RecCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    def get_product_reviews(self, instance):
        reviews = instance.productreview.all()
        review_ser = ProductRatingSerializer(reviews, many=True)
        return review_ser.data

    def get_average_rating(self, instance):
        ratings = ProductRating.objects.filter(product=instance)
        avg_rating = ratings.aggregate(Avg('star'))['star__avg']
        return avg_rating

    class Meta:
        model = Product
        fields = "__all__"
        

class GetProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    product_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    rec_category = RecCategorySerializer(read_only=True)  # Bu yerda o'zgartirish qilindi
    category = RecCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    def get_product_reviews(self, instance):
        reviews = instance.productreview.all()  # Adjust the related name if necessary
        return ProductRatingSerializer(reviews, many=True).data

    def get_average_rating(self, instance):
        ratings = ProductRating.objects.filter(product=instance)
        avg_rating = ratings.aggregate(Avg('star'))['star__avg']
        return avg_rating
    
    def get_related_products(self, instance):
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]  # Get 5 related products
        return ProductSerializer(related_products, many=True, context=self.context).data

    def to_representation(self, instance):
        serialized_product = super().to_representation(instance)
        serialized_product['related_products'] = self.get_related_products(instance)
        return serialized_product

    class Meta:
        model = Product
        fields = "__all__"
