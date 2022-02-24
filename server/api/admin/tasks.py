from celery import shared_task
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template.loader import render_to_string
from server.models.user import User


@shared_task
def add_users(user_list, send_welcome_email=False):
    for new_user in user_list:
        password = new_user.get('password', 'password')
        user = User(**new_user)
        user.set_password(password)
        user.save()

        if send_welcome_email:
            email = new_user.get('email')
            subject = 'Welcome to LearnBasket'
            message = render_to_string('welcome_email.html', {**new_user})
            try:
                send_mail(
                    subject=subject, 
                    message=message, 
                    from_email='support@learnbasket.com', 
                    recipient_list=[email], 
                    fail_silently=False
                )
            except SMTPException:
                print('SMTP Error')
