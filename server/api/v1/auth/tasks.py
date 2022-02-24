from email import message
from celery import shared_task
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template.loader import render_to_string


@shared_task
def send_verification_email(user_data, verify_url):
    email = user_data.get('email')
    subject = 'Welcome to Techowiz'
    message = render_to_string('verification_email.html', {
                    **user_data,
                    'verify_url': verify_url, 
                })
    try:
        send_mail(subject=subject, message=message, from_email='support@learnbasket.com', recipient_list=[email], fail_silently=False)
    except SMTPException:
        print('SMTP Error')

@shared_task
def send_welcome_email(user_data):
    email = user_data.get('email')
    subject = 'Welcome to LearnBasket'
    message = render_to_string('welcome_email.html', {**user_data})
    try:
        send_mail(subject=subject, message=message, from_email='support@learnbasket.com', recipient_list=[email], fail_silently=False)
    except SMTPException:
        print('SMTP Error')