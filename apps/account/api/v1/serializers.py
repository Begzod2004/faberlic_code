# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
# from rest_framework import serializers
# from rest_framework.exceptions import AuthenticationFailed
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.crypto import get_random_string
# from apps.account.models import Account, OTP
# import random
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.utils.encoding import  smart_str, force_str
# from django.utils.encoding import smart_bytes

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=6, max_length=68, write_only=True)
#     password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

#     class Meta:
#         model = Account
#         fields = ('full_name', 'phone','email', 'password', 'password2')

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')

#         if password != password2:
#             raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
#         return attrs

#     def create(self, validated_data):
#         del validated_data['password2']
#         user = Account.objects.create_user(**validated_data)
#         user.is_active = False  # Deactivate account till OTP is verified
#         user.save()

#         # Generate a 4-digit OTP without using 'digits' argument
#         otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
#         OTP.objects.create(account=user, otp=otp)

#         # Send OTP via email
#         email_body = f'Hi {user.full_name},\n\nYour OTP for account activation is: {otp}\n\nBest,\nYour Team'
#         send_mail(
#             'Account Activation OTP',
#             email_body,
#             'from@yourdomain.com',
#             [user.email],
#             fail_silently=False,
#         )
#         return user

# # OTP Verification Serializer
# # class OTPVerificationSerializer(serializers.Serializer):
# #     email = serializers.EmailField()
# #     otp = serializers.CharField(max_length=4)

# #     class Meta:
# #         model = Account
# #         fields = ('email', 'otp')

# #     def validate(self, attrs):
# #         email = attrs.get('email')
# #         otp = attrs.get('otp')

# #         try:
# #             user = Account.objects.get(email=email)
# #             otp_instance = OTP.objects.filter(account=user, otp=otp).last()

# #             if otp_instance is None or otp_instance.is_expired():
# #                 raise serializers.ValidationError("Invalid or expired OTP.")
# #             user.is_active = True
# #             user.save()
# #         except Account.DoesNotExist:
# #             raise serializers.ValidationError("User not found.")
# #         return attrs


# class OTPVerificationSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=4)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         otp = attrs.get('otp')

#         try:
#             user = Account.objects.get(email=email)
#             otp_instance = OTP.objects.filter(account=user, otp=otp).last()

#             if otp_instance is None or otp_instance.is_expired():
#                 raise serializers.ValidationError("Invalid or expired OTP.")
            
#             # Foydalanuvchi obyektini 'validated_data'ga qo'shish
#             attrs['user'] = user
#         except Account.DoesNotExist:
#             raise serializers.ValidationError("User not found.")
#         return attrs

#     def save(self, **kwargs):
#         user = self.validated_data['user']
#         user.is_active = True  # Foydalanuvchi hisobini faollashtirish
#         user.save()




# User = get_user_model()

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

#     def validate(self, data):
#         try:
#             user = User.objects.get(email=data['email'])
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User with this email does not exist.")
        
#         if not user.check_password(data['password']):
#             raise serializers.ValidationError("Incorrect password.")

#         if not user.is_active:
#             raise serializers.ValidationError("This account is inactive.")
        
#         # Agar barcha tekshiruvlar muvaffaqiyatli bo'lsa, user obyektini qaytaramiz
#         data['user'] = user
#         return data
    
# class EmailVerificationSerializer(serializers.ModelSerializer):
#     tokens = serializers.CharField(max_length=555)

#     class Meta:
#         model = Account
#         fields = ('tokens',)


# class ResetPasswordSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()

#     class Meta:
#         model = Account
#         fields = ('email',)


# class AccountUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('id', 'full_name', 'image_url', 'email', 'phone',)


# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('id', 'full_name',)


# class AccountOwnImageUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('image',)


# class SetNewPasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     uidb64 = serializers.CharField(max_length=68, required=True)
#     token = serializers.CharField(max_length=555, required=True)

#     class Meta:
#         model = Account
#         fields = ('password', 'password2', 'uidb64', 'token')

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         uidb64 = attrs.get('uidb64')
#         token = attrs.get('token')
#         _id = force_str(urlsafe_base64_decode(uidb64))
#         user = Account.objects.filter(id=_id).first()
#         current_password = user.password
#         if not PasswordResetTokenGenerator().check_token(user, token):
#             raise AuthenticationFailed({'success': False, 'message': 'The token is not valid'})
#         if password != password2:
#             raise serializers.ValidationError({
#                 'success': False, 'message': 'Password did not match, please try again'
#             })

#         if check_password(password, current_password):
#             raise serializers.ValidationError(
#                 {'success': False, 'message': 'New password should not similar to current password'})

#         user.set_password(password)
#         user.save()
#         return attrs


# class ChangeNewPasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     password = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

#     class Meta:
#         model = Account
#         fields = ('old_password', 'password', 'password2')

#     def validate(self, attrs):
#         old_password = attrs.get('old_password')
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         request = self.context.get('request')
#         user = request.user
#         if not user.check_password(old_password):
#             print(55555555)
#             raise serializers.ValidationError(
#                 {'success': False, 'message': 'Old password did not match, please try again new'})

#         if password != password2:
#             print(321)
#             raise serializers.ValidationError(
#                 {'success': False, 'message': 'Password did not match, please try again new'})

#         user.set_password(password)
#         user.save()
#         return attrs
