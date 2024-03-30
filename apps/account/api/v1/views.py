# import jwt
# from django.conf import settings
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.db.models import Q
# from django.contrib.auth import login
# from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from drf_yasg import openapi
# from rest_framework import generics, status, views
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from apps.account.api.v1.permissions import IsOwnUserOrReadOnly
# # from apps.account.api.v1.permissions import IsOwnUserOrReadOnly
# from apps.account.api.v1.serializers import RegisterSerializer, LoginSerializer, AccountUpdateSerializer, \
#     AccountOwnImageUpdateSerializer, SetNewPasswordSerializer,  ResetPasswordSerializer, \
#     ChangeNewPasswordSerializer
# from apps.account.api.v1.utils import Util
# from apps.account.models import Account
# from rest_framework import generics, status
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from apps.account.models import Account
# from apps.account.api.v1.serializers import RegisterSerializer, OTPVerificationSerializer, LoginSerializer
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from django.contrib.auth import authenticate
# from rest_framework import serializers
# from django.contrib.auth import get_user_model


# class AccountRegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'success': True, 'message': 'Account created. Please check your email for the OTP to activate your account.'}, status=status.HTTP_201_CREATED)


#     # @swagger_auto_schema(request_body=OTPVerificationSerializer,
#     #                      responses={200: 'Account activated successfully', 400: 'Invalid request'})

    


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)  # Foydalanuvchini tizimga kiritish
#             return Response({'success': True, 'message': 'You are successfully logged in.'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class OTPVerificationView(APIView):
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(request_body=OTPVerificationSerializer,
#                          responses={200: 'Account activated successfully', 400: 'Invalid request'})
#     def post(self, request, *args, **kwargs):
#         serializer = OTPVerificationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # Bu yerda foydalanuvchi hisobini faollashtirish amalga oshiriladi
#             return Response({'success': True, 'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # class LoginAPIView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request, *args, **kwargs):
# #         serializer = LoginSerializer(data=request.data)
# #         if serializer.is_valid(raise_exception=True):
# #             return Response(serializer.validated_data, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class AccountRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#     # http://127.0.0.1:8000/api/account/v1/retrieve-update/<id>/
#     serializer_class = AccountUpdateSerializer
#     queryset = Account.objects.all()
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

#     def get(self, request, *args, **kwargs):
#         query = self.get_object()
#         if query:
#             serializer = self.get_serializer(query)
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({'success': False, 'message': 'query did not exist'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, *args, **kwargs):
#         obj = self.get_object()
#         serializer = self.get_serializer(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
#         return Response({'success': False, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)


# class SetPasswordConfirmAPIView(views.APIView):
#     # http://127.0.0.1:8000/account/set-password-confirm/<uidb64>/<token>/
#     permission_classes = (AllowAny,)

#     def get(self, request, uidb64, token):
#         try:
#             _id = smart_str(urlsafe_base64_decode(uidb64))
#             user = Account.objects.filter(id=_id).first()
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'success': False, 'message': 'Token is not valid, please try again'},
#                                 status=status.HTTP_406_NOT_ACCEPTABLE)
#         except DjangoUnicodeDecodeError as e:
#             return Response({'success': False, 'message': f'DecodeError: {e.args}'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token},
#                         status=status.HTTP_200_OK)


# class SetNewPasswordView(generics.UpdateAPIView):
#     # http://127.0.0.1:8000/api/account/v1/set-password/
#     serializer_class = SetNewPasswordSerializer
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

#     def patch(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)


# class ResetPasswordAPIView(generics.GenericAPIView):
#     # http://127.0.0.1:8000/account/v1/reset-password/
#     serializer_class = ResetPasswordSerializer

#     def post(self, request):
#         user = Account.objects.filter(email=request.data['email']).first()

#         if user:
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = 'makssss.pythonanywhere.com/'
#             abs_url = f'http://{current_site}account/v1/set-password-confirm/{uidb64}/{token}/'
#             email_body = f'Hello, \n User link below to activate your email \n {abs_url}'
#             data = {
#                 'to_email': user.email,
#                 'email_subject': 'Reset password',
#                 'email_body': email_body
#             }
#             Util.send_email(data)

#             return Response({'success': True, 'message': 'Link sent to email'}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'Email did not match'}, status=status.HTTP_400_BAD_REQUEST)


# class AccountView(generics.RetrieveAPIView):
#     # http://127.0.0.1:8000/api/account/v1/get-account/
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated,)
#     serializer_class = AccountUpdateSerializer

#     def queryset(self, request, *args, **kwargs):
#         user = request.user
#         query = Account.objects.get(id=user.id)
#         serializer = self.get_serializer(query)
#         return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


# class AccountOwnImageUpdateView(generics.RetrieveUpdateAPIView):
#     # http://127.0.0.1:8000/api/account/v1/image-retrieve-update/<id>/
#     serializer_class = AccountOwnImageUpdateSerializer
#     queryset = Account.objects.all()
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

#     def get(self, request, *args, **kwargs):
#         query = self.get_object()
#         if query:
#             serializer = self.get_serializer(query)
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'query does not match'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, *args, **kwargs):
#         obj = self.get_object()
#         serializer = self.get_serializer(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)


# class AccountListView(generics.ListAPIView):
#     # http://127.0.0.1:8000/api/account/v1/list/
#     serializer_class = AccountUpdateSerializer
#     queryset = Account.objects.all()
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         qs = super().get_queryset()
#         q = self.request.GET.get('q')

#         q_condition = Q()
#         if q:
#             q_condition = Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q)

#         queryset = qs.filter(q_condition)

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if queryset:
#             serializer = self.get_serializer(queryset, many=True)
#             count = queryset.count()
#             return Response({'success': True, 'count': count, 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'data': 'queryset does not match'}, status=status.HTTP_404_NOT_FOUND)


# class ChangePasswordCompletedView(generics.UpdateAPIView):
#     # http://127.0.0.1:8000/account/change-password/
#     queryset = Account.objects.all()
#     serializer_class = ChangeNewPasswordSerializer
#     permission_classes = (IsAuthenticated,)
#     lookup_field = 'pk'

#     def patch(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
