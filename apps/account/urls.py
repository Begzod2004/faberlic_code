from django.urls import path
from .views import SendVerificationEmailView, VerifyCodeView

urlpatterns = [
    path('send_verification_email/', SendVerificationEmailView.as_view(), name='send_verification_email'),
    path('api/verify_code/', VerifyCodeView.as_view(), name='verify_code'),
]


# Umumiy Maslahatlar:
# Tokenlarni Qaytarish: Hozirgi kodda foydalanuvchilarni ro'yxatdan o'tkazgandan so'ng, faqat muvaffaqiyatli ro'yxatdan o'tish haqida xabar qaytarilmoqda. Siz, shuningdek, foydalanuvchiga JWT tokenlarni (access va refresh tokenlar) ham qaytarishingiz mumkin. Bu, frontendda foydalanuvchini darhol tizimga kiritish imkonini beradi.

# python
# Copy code
# if serializer.is_valid():
#     user = serializer.save()
#     tokens = serializer.get_tokens(user)
#     return Response({"message": "User registered successfully.", "tokens": tokens}, status=status.HTTP_201_CREATED)
# Serializerdan Qaytarilgan Ma'lumotlarni Qaytarish: Serializerdan qaytarilgan ma'lumotlarni (masalan, foydalanuvchi IDsi, emaili va h.k.) ham qaytarishingiz mumkin. Bu, frontendda foydalanuvchining profil ma'lumotlarini darhol ko'rsatish imkonini beradi.

# Xavfsizlik Masalalari: Email yuborish va parollar bilan ishlashda xavfsizlikni yaxshilash uchun Django'ning xavfsizlik amaliyotlarini ko'rib chiqing. Masalan, parolni email orqali yuborish o'rniga, foydalanuvchiga parolni o'rnatish yoki tiklash uchun havola yuborishingiz mumkin.