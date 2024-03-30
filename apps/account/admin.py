from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Foydalanuvchilarni ko'rish va tahrirlash uchun ishlatiladigan maydonlar
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('is_active',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'code_sent_at')}),
    )
    # Ro'yxatdan o'tish formasi uchun ishlatiladigan maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')  # Admin ro'yxatida ko'rsatiladigan ustunlar
    search_fields = ('email',)  # Qidiruv maydoni orqali qidiriladigan maydonlar
    ordering = ('email',)  # Saralash uchun asosiy maydon

# User modelini admin interfeysida ro'yxatdan o'tkazish
admin.site.register(User, UserAdmin)
