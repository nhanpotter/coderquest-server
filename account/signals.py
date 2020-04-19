from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Avatar

@receiver(post_save, sender=Avatar)
def level_up(sender, **kwargs):
    avatar = kwargs['instance']

    if avatar.experience < 100:
        return
    
    while avatar.experience > 100:
        avatar.experience -= 100
        avatar.level += 1

    avatar.save()