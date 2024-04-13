from celery import shared_task

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail

import datetime
import requests


User = get_user_model()
token = "6785944157:AAFq7gvVo27CSfNmjhavD_k6MGDBaPhNsJ8"


@shared_task(bind=True)
def check_subscriptions(a):
    for user in User.objects.all():
        if user.subscription_start and user.subscription_type != User.NONE:
            if user.subscription_type == User.MONTHLY and timezone.now() > user.subscription_start + datetime.timedelta(days=30):
                if user.telegram_chat_id:
                    send_telegram_notification(user.telegram_chat_id, f'Здраствуйте, {user.username}!\nВаша подписка к сожалению истекла!\nВы можете её продлить!')
                send_mail_ending_subs(user)
                user.subscription_type = User.NONE
                user.subscription_start = None
            elif user.subscription_type == User.YEARLY and timezone.now() > user.subscription_start + datetime.timedelta(days=365):
                if user.telegram_chat_id:
                    send_telegram_notification(user.telegram_chat_id, f'Здраствуйте, {user.username}!\nВаша подписка к сожалению истекла!\nВы можете её продлить!')
                send_mail_ending_subs(user)
                user.subscription_type = User.NONE
                user.subscription_start = None
            user.save()


@shared_task(bind=True)
def send_message(a):
    for user in User.objects.all():
        if user.subscription_type == User.MONTHLY:
            subscription_end = user.subscription_start + datetime.timedelta(days=30)
            if timezone.now() > subscription_end - datetime.timedelta(days=7) and subscription_end > timezone.now():
                if user.telegram_chat_id:
                    send_telegram_notification(user.telegram_chat_id, f'Здраствуйте, {user.username}! \nВаша подписка истечет в {subscription_end} \nМожете продлить её!')
                send_email_notification(user, subscription_end)
        elif user.subscription_type == User.YEARLY:
            subscription_end = user.subscription_start + datetime.timedelta(days=365)
            if timezone.now() > subscription_end - datetime.timedelta(days=7) and timezone.now() < subscription_end:
                if user.telegram_chat_id:
                    send_telegram_notification(user.telegram_chat_id, f'Здраствуйте, {user.username}! \nВаша подписка истечет в {subscription_end} \nМожете продлить её!')
                send_email_notification(user, subscription_end)


def send_telegram_notification(chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)


def send_email_notification(user, end):
    send_mail(
        f'Здраствуйте, {user.username}!',
        f'Здраствуйте, {user.username}!\nВаша подписка истечет в {end} \n Можете продлить её!',
        'shamsutdinovanvar21@gmail.com',
        [user.email],
        fail_silently=False,
    )


def send_mail_ending_subs(user):
    send_mail(
        f'Здраствуйте, {user.username}!',
        f'Здраствуйте, {user.username}!\nВаша подписка к сожалению истекла! \n Можете продлить её!',
        'shamsutdinovanvar21@gmail.com',
        [user.email],
        fail_silently=False,
    )


