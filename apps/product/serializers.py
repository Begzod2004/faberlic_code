from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import  Product, Category, SubCategory, ProductImage, ProductRating
from rest_framework import serializers
from django.db.models import Avg


class SubCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SubCategory)
    
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer'

    def get_subcategory(self, category_instance):
        subcategories = SubCategory.objects.filter(category=category_instance)
        serializer = SubCategorySerializer(subcategories, many=True)
        return serializer.data
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
    
    
class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category = SubCategorySerializer(read_only=True)
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
    category = SubCategorySerializer(read_only=True)
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
    category = SubCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)



    def to_representation(self, instance):
        serialized_product = super().to_representation(instance)
        serialized_product['related_products'] = self.get_related_products(instance)
        return serialized_product

    class Meta:
        model = Product
        fields = "__all__"



