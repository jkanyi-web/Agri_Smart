from django.core.mail import send_mail
from django.conf import settings

def send_registration_email(user_email):
    subject = 'Welcome to Agri Smart'
    message = 'Thank you for registering with Agri Smart.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
