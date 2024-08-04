# from django.contrib import admin
# from .models import Category, SubCategory, Brand, Product, Banner, IndexCategory, Stock
# from modeltranslation.admin import TranslationAdmin

# class CategoryAdmin(TranslationAdmin):
#     list_display = ('title', 'is_index')
#     search_fields = ['title']

# class SubCategoryAdmin(TranslationAdmin):
#     list_display = ('title', 'category')
#     search_fields = ['title']
#     list_filter = ('category',)

# class BrandAdmin(TranslationAdmin):
#     list_display = ('title',)
#     search_fields = ['title']

# class ProductAdmin(TranslationAdmin):
#     list_display = ('title', 'price', 'category', 'brand', 'is_available')
#     search_fields = ['title', 'description']
#     list_filter = ('is_available', 'category', 'brand')
#     prepopulated_fields = {"slug": ("title",)}

# class BannerAdmin(TranslationAdmin):
#     list_display = ('category', 'is_advertisement')
#     list_filter = ('is_advertisement',)

# class IndexCategoryAdmin(TranslationAdmin):
#     list_display = ('title', 'category')
#     list_filter = ('category',)

# class StockAdmin(TranslationAdmin):
#     list_display = ('title',)
#     search_fields = ['title']

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(SubCategory, SubCategoryAdmin)
# admin.site.register(Brand, BrandAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Banner, BannerAdmin)
# admin.site.register(IndexCategory, IndexCategoryAdmin)
# admin.site.register(Stock, StockAdmin)
