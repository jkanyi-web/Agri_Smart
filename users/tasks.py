from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_registration_email(user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    subject = 'Welcome to AgriSmart'
    message = f'Hi {user.username}, thank you for registering at AgriSmart.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
