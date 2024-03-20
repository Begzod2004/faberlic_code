from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Sizning mavjud kategoriyalar va subkategoriyalar uchun modellaringiz
class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_('Name')),
    )
    image = models.ImageField(upload_to='category_images', verbose_name=_('Rasm'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def subcategories(self):
        return SubCategory.objects.filter(category=self)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class SubCategory(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_('Name')),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Parent Category'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name    

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')

# Mahsulot modeli
class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=300, verbose_name=_('Nomi')),
        description=RichTextField(),
        tag=models.TextField(verbose_name=_('Tag')),
        short_description=models.CharField(max_length=300, null=True, blank=True, default="NEW"),
    )
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name=_('Kategorylari'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('MAXSULOT')
        verbose_name_plural = _('Mahsulotlar')
        ordering = ['-created_at']

# Mahsulot rasmlari uchun model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"Image for {self.product.name}"
    

class ProductRating(models.Model):
    name = models.CharField(max_length=123, help_text="Nomi")
    star = models.IntegerField(default=0 , verbose_name = "star")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productreview')
    review_comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True, verbose_name='review_created_date')
    email = models.EmailField()

    class Meta:
        verbose_name = _('Product Rating')
        verbose_name_plural = _('Product Ratings')

    def __str__(self):
        return f"{self.product.name} - {self.star} stars"



# Yangi qo'shilgan Buyurtma va Buyurtma bandlari uchun modellar
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'))
    phone_number = PhoneNumberField(verbose_name=_('Telefon Raqami'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan Vaqti'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yangilangan Vaqti'))
    is_processed = models.BooleanField(default=False, verbose_name=_('Qayta ishlandimi?'))

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = _('Buyurtma')
        verbose_name_plural = _('Buyurtmalar')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Buyurtma'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Mahsulot'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Miqdori'))

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = _('Buyurtma Bandidagi Mahsulot')
        verbose_name_plural = _('Buyurtma Bandidagi Mahsulotlar')
