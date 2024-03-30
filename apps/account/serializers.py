from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
# from .utils import generate_password, send_password_email  # O'zgaruvchilarni oldindan yaratgan funksiyalaringiz

User = get_user_model()



class VerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already verified.")
        return value


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], verification_code=data['code'], is_active=False)
            if not user.code_sent_at or timezone.now() > user.code_sent_at + timezone.timedelta(minutes=10):
                raise serializers.ValidationError("Verification code is expired or invalid.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or verification code.")
        return data



