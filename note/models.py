from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from workshop.models import Workshop, Tailoring, Report


User = get_user_model()


class Notepad(models.Model):
    workshop = models.OneToOneField(Workshop, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Цех"))
    body = RichTextField(verbose_name=_("Текст блокнота"), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Блокнот")
        verbose_name_plural = _("Блокноты")

    def __str__(self):
        return f"{self.body} - {self.workshop.title}"


class TailoringComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Владелец комментария"))
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Цех"))

    tailoring = models.ForeignKey(Tailoring, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Связь с пошивом"))
    body = RichTextField(blank=True, null=True, verbose_name=_("Текст комментария"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Комментарий к пошиву")
        verbose_name_plural = _("Комментарии к пошиву")

    def __str__(self):
        return f"{self.body} - {self.owner.first_name} {self.owner.last_name}"


class ReportComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Владелец комментария"))
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Цех"))

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Связь с отчетом"))
    body = RichTextField(blank=True, null=True, verbose_name=_("Текст комментария"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Комментарий к отчету")
        verbose_name_plural = _("Комментарии к отчету")

    def __str__(self):
        return f"{self.body} - {self.owner.first_name} {self.owner.last_name}"
