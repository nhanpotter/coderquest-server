from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import World, NPC, User_NPC, User_World

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_world_history_for_new_user(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    if not user.is_staff:
        world_list = World.objects.all()
        if len(world_list) != 0:
            for world in world_list:
                User_World.objects.create(
                    user=user,
                    world=world,
                    is_finished=False
                )


@receiver(post_save, sender=World)
def create_user_world_history_for_new_world(sender, **kwargs):
    world = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    user_list = User.objects.filter(is_staff=False)
    for user in user_list:
        User_World.objects.create(
            user=user,
            world=world,
            is_finished=False
        )


@receiver(post_save, sender=User)
def create_user_NPC_history_for_new_user(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    if not user.is_staff:
        npc_list = NPC.objects.all()
        if (len(npc_list)!=0):
            for npc in npc_list:
                User_NPC.objects.create(
                    is_defeated=False,
                    user=user,
                    npc=npc
                )

@receiver(post_save, sender=NPC)
def create_user_NPC_history_for_new_NPC(sender, **kwargs):
    npc = kwargs['instance']
    created = kwargs['created']
    if not created:
        return
        
    user_list = User.objects.filter(is_staff=False)
    for user in user_list:
        User_NPC.objects.create(
            user=user,
            npc=npc,
            is_defeated=False
        )
