from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

import uuid


class CustomUser(AbstractUser):
    NONE = 'N'
    YEARLY = 'Y'
    MONTHLY = 'M'

    SUBSCRIPTION_CHOICES = [
        (NONE, _('Без подписки')),
        (YEARLY, _('Годовая')),
        (MONTHLY, _('Месячная')),
    ]

    REGISTER_CHOISES = [
        ('worker', _('Работник')),
        ('head', _('Владелец цеха'))
    ]

    email = models.EmailField(_("Электронная почта"), unique=True)
    phone = PhoneNumberField(verbose_name=_("Номер телефона"), help_text='Пример: +996700777777', null=True, blank=True)
    about_me = models.TextField(blank=True, null=True, verbose_name=_("О себе"))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))
    telegram_chat_id = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Айди чата"), default=None)
    account_type = models.CharField(max_length=10, choices=REGISTER_CHOISES, default='head', verbose_name=_('Тип аккаунта'))
    subscription_type = models.CharField(max_length=1, choices=SUBSCRIPTION_CHOICES, default=NONE, verbose_name=_("Тип подписки"))
    subscription_start = models.DateTimeField(blank=True, null=True, verbose_name=_("Начало подписки"))
    unique_link = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_link:
            self.unique_link = str(uuid.uuid4())
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
