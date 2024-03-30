# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserRegistrationSerializer, SendVerificationEmailSerializer , VerifyCodeSerializer

# class UserRegistrationView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully, please check your email for the password."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SendVerificationEmailView(APIView):
#     def post(self, request):
#         serializer = SendVerificationEmailSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             # Emailga kod yuborish logikasi
#             return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VerifyCodeAndLoginView(APIView):
#     def post(self, request):
#         serializer = VerifyCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             # Foydalanuvchini tasdiqlash va tokenlarni qaytarish logikasi
#             return Response({"token": "your_jwt_token_here"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerificationEmailSerializer, VerifyCodeSerializer
from .models import User
from apps.account.utils import send_verification_email, generate_verification_code  # Bu funksiyalarni alohida yaratishingiz kerak
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class SendVerificationEmailView(APIView):
    def post(self, request):
        serializer = VerificationEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user, created = User.objects.get_or_create(email=email)
            if not created and user.is_active:
                return Response({"message": "This email is already verified."}, status=status.HTTP_400_BAD_REQUEST)
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.code_sent_at = timezone.now()
            user.save()
            send_verification_email(email, verification_code)  # Bu funksiyani alohida yaratishingiz kerak
            return Response({"message": "Verification email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.is_active = True
            user.verification_code = None  # Kodni tozalash
            user.save()
            # JWT tokenlarni qaytarish
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
