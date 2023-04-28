from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def category_games_amount_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.category.post_amount += 1
        instance.category.save()


@receiver(post_delete, sender=Post)
def category_games_amount_post_delete(sender, instance, *args, **kwargs):
    instance.category.post_amount -= 1
    instance.category.save()
