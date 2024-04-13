from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from workshop.models import Report


@receiver(m2m_changed, sender=Report.expenses.through)
def update_expenses_total(sender, instance, **kwargs):
    if kwargs['action'] in ['post_add', 'post_remove', 'post_clear']:
        instance.expenses_total = sum(instance.expenses.values_list('value', flat=True))
        instance.save()
