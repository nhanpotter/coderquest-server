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
    
    world = npc.world
    user_list = User.objects.filter(is_staff=False)
    for user in user_list:
        User_NPC.objects.create(
            user=user,
            npc=npc,
            is_defeated=False
        )
        user_world = User_World.objects.get(user=user, world=world)
        if user_world.is_finished:
            user_world.is_finished = False
            user_world.save()


@receiver(post_save, sender=User_NPC)
def check_User_World_when_User_NPC_updated(sender, **kwargs):
    user_npc = kwargs['instance']
    created = kwargs['created']
    if created:
        # If newly created, don't need to check
        return

    user = user_npc.user
    world = user_npc.npc.world

    is_finished = True
    user_npc_history = User_NPC.objects.filter(user=user, npc__world=world)

    for history in user_npc_history:
        is_finished = history.is_defeated
        if not is_finished:
            break

    if is_finished:
        user_world = User_World.objects.get(user=user, world=world)
        user_world.is_finished = True
        user_world.save()
