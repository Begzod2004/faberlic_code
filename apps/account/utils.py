import random
import string
# Foydalanuvchiga parol yuborish uchun
from django.core.mail import send_mail


import random

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)