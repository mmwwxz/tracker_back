from django.core.mail import send_mail
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from config import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        subject = 'Password Reset for Track.'
        token = reset_password_token.key
        message = f'''Здравствуйте, {reset_password_token.user.username}!
Вставьте этот токен на сайте.\n
                {token}\n
Для сброса пароля и введите новый пароль.
'''
        from_email = settings.EMAIL_HOST_USER
        to_email = reset_password_token.user.email
        send_mail(subject, message, from_email, [to_email])
    except Exception as e:
        print(f"Error sending password reset email: {e}")
