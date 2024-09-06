from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from services.models import Counseling, Session, Visit
from restates.models import TradeSession


@receiver(post_save, sender=TradeSession)
def create_task_for_trade_session(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_trade_session=instance)


@receiver(post_save, sender=Counseling)
def create_task_for_counseling(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_counseling=instance)


@receiver(post_save, sender=Session)
def create_task_for_session(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_session=instance)


@receiver(post_save, sender=Visit)
def create_task_for_visit(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_visit=instance)



