from django.contrib import admin
from .models import Category, Product, SubCategory, ProductImage, Order, OrderItem, ProductRating

from parler.admin import TranslatableAdmin
from django.utils.html import format_html

class CategoryAdmin(TranslatableAdmin):
    list_display = ['name']
    list_display_links = ['name',]
    search_fields = ['name']
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'image'),
        }),
    )

admin.site.register(Category, CategoryAdmin)



class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(TranslatableAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'created_at','short_description', 'is_featured']
    list_display_links = ['name']
    search_fields = ['name',  'tag'] 
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)



    fieldsets = (
        (None, {
            'fields': ('name','description', 'tag', 'category',  'is_featured', 'short_description'),
        },),
    )

admin.site.register(Product, ProductAdmin)



@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['name','product', 'star', 'review_date', 'email']
    list_filter = ['star']
    search_fields = ['product__name', 'email']
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('name','product', 'star', 'review_comment', 'review_date', 'email'),
        }),
    )
    readonly_fields = ['review_date']


class SubCategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'category', 'is_active']
    list_display_links = ['name']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'is_active']
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'is_active'),
        }),
    )

admin.site.register(SubCategory, SubCategoryAdmin)




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Qo'shimcha bo'sh bandlar soni
    fields = ['product', 'quantity']
    readonly_fields = ['product', 'quantity']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'phone_number', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['user__username', 'phone_number']
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Order, OrderAdmin)
