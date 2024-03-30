# from django.utils.translation import gettext_lazy as _  # Qo'shilgan qator
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils import timezone

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)

# from django.contrib.auth.models import User
# from django.db import models

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     verification_code = models.CharField(max_length=6, blank=True, null=True)  # Tasdiqlash kodini saqlash uchun maydon
#     code_sent_at = models.DateTimeField(null=True, blank=True)  # Kod yuborilgan vaqtni saqlash uchun maydon

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#      # `groups` va `user_permissions` uchun `related_name` qo'shish
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name=_('groups'),
#         blank=True,
#         related_name="%(app_label)s_%(class)s_groups",  # Bu yerda o'zgartirish
#         related_query_name="%(app_label)s_%(class)s",
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name=_('user permissions'),
#         blank=True,
#         related_name="%(app_label)s_%(class)s_user_permissions",  # Bu yerda o'zgartirish
#         related_query_name="%(app_label)s_%(class)s",
#     )

#     def __str__(self):
#         return self.email

#     def __str__(self):
#         return self.email


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    verification_code = models.CharField(max_length=16, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

