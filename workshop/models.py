from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
import decimal


User = get_user_model()


class Workshop(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    description = RichTextField(blank=True, null=True, verbose_name=_("Описание"))

    head = models.ForeignKey(User, on_delete=models.CASCADE, related_name='head_workshops', verbose_name=_("Руководитель"), blank=True, null=True)
    workers = models.ManyToManyField(User, related_name='workers_workshops', blank=True, verbose_name=_("Сотрудники"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self):
        return f"{self.title} - {self.head.first_name} {self.head.last_name}"

    class Meta:
        verbose_name = _("Цех")
        verbose_name_plural = _("Цеха")


class Tailoring(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Автор записи"))
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Цех"))

    model = models.CharField(max_length=255, verbose_name=_("Модель"))
    master = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Мастер"))

    quantity = models.PositiveSmallIntegerField(default=1, blank=True, null=True, verbose_name=_("Количество"))
    master_unit_price = models.DecimalField(default=1, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Цена за единицу работы мастера"))

    done = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name=_("Выполнено"))
    total_master_payment = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Общая оплата мастеру"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self):
        return f"{self.model} - {self.master}"

    class Meta:
        verbose_name = _("Пошив")
        verbose_name_plural = _("Пошивы")

    def save(self, *args, **kwargs):
        self.total_master_payment = self.master_unit_price * self.done
        super().save(*args, **kwargs)
        for report in self.reports.all():
            report.save()


class Expense(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='expenses', verbose_name=_("Автор записи"))
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, blank=True, null=True, related_name='expenses', verbose_name=_("Цех"))

    title = models.CharField(max_length=255, verbose_name=_("Название расхода"))
    value = models.DecimalField(default=1, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Сумма расхода"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self):
        return f"{self.title} - {self.value}"

    class Meta:
        verbose_name = _("Расход")
        verbose_name_plural = _("Расходы")


class Report(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='reports', verbose_name=_("Автор записи"))
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, blank=True, null=True, related_name='reports', verbose_name=_("Цех"))

    tailoring = models.ForeignKey(Tailoring, on_delete=models.CASCADE, related_name='reports', verbose_name=_("Пошив"))
    expenses = models.ManyToManyField(Expense, related_name='reports', blank=True, verbose_name=_("Расходы"))

    expenses_total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Общая сумма расходов"))
    production_total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Общая стоимость производства"))
    production_unit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Стоимость производства за единицу"))

    unit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Цена продажи за единицу"))
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Общая сумма для продажи"))

    margin = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Маржа"))
    profit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Прибыль"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self):
        return f"Отчет от {self.created_at.strftime('%Y-%m-%d')} - {self.workshop.title}"

    class Meta:
        verbose_name = _("Отчет")
        verbose_name_plural = _("Отчеты")

    def save(self, *args, **kwargs):
        self.production_total = self.expenses_total + self.tailoring.total_master_payment
        if self.tailoring.done and self.tailoring.done > 0:
            self.production_unit = self.production_total / self.tailoring.done
        else:
            self.production_unit = decimal.Decimal(0)
        self.unit = self.production_unit + self.margin
        self.total = self.unit * self.tailoring.done
        self.profit = self.total - self.production_total
        super().save(*args, **kwargs)
