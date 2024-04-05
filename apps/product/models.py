from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField
# from django.contrib.auth.models import User
from apps.accounts.models import User


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_('Name')),
        description=RichTextField(default=None),

    )
    image = models.ImageField(upload_to='category_images', verbose_name=_('Rasm'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def reccategories(self):
        return RecCategory.objects.filter(category=self)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class RecCategory(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_('Name')),
    )
    image = models.ImageField(upload_to='recctegory_images', verbose_name=_('Rasm'), blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name    

    class Meta:
        verbose_name = _('Reccategory')
        verbose_name_plural = _('Reccategories')

# Mahsulot modeli
class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=300, verbose_name=_('Nomi')),
        description=RichTextField(),
        tag=models.TextField(verbose_name=_('Tag'), default='Women'),
        short_description=models.CharField(max_length=300, null=True, blank=True, default="NEW"),
    )
    rec_category = models.ForeignKey(RecCategory, on_delete=models.CASCADE, verbose_name=_('Rekamindatsiya Kategoriyasi'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Product Kategory'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Narxi'))  # Narx maydoni qo'shildi
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
    is_processed = models.BooleanField(default=True, verbose_name=_('Qayta ishlandimi?'))

    def __str__(self):
        return f"{self.user.first_name} - {self.created_at.strftime('%Y-%m-%d')}"

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
