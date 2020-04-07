from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from course.models import Course, Section, QuestionBank

User = get_user_model()

class Expedition(models.Model):
    # Mapping
    course = models.OneToOneField(Course, on_delete=models.CASCADE)

    def __str__(self):
        return 'Expedition {0}-{1}'.format(self.id, self.course.course_code)

    def __unicode__(self):
        return 'Expedition {0}-{1}'.format(self.id, self.course.course_code)

    def get_worlds(self):
        worlds = self.world_set.all()
        worlds = worlds.order_by('level')

        return worlds
    
    worlds = property(get_worlds)


class World(models.Model):
    background_type = models.IntegerField()   

    # Mapping
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE)
    section = models.OneToOneField(Section, on_delete=models.CASCADE)

    def __str__(self):
        return 'Expedition:({0}) Section:({1})'.format(str(self.expedition), str(self.section))

    def __unicode__(self):
        return 'Expedition:({0}) Section:({1})'.format(str(self.expedition), str(self.section))

    def get_npcs(self):
        return self.npc_set.all()

    npcs = property(get_npcs)


class User_World(models.Model):
    """
    Table to keep track history whether user has finished the world or not
    """
    is_finished = models.BooleanField()
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

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

class NPCAvatar(models.Model):
    hp = models.IntegerField()
    attack = models.IntegerField()
    npc_type = models.IntegerField()

    def __str__(self):
        return 'HP:{0}-Attack:{1}-Type:{2}'.format(self.hp, self.attack, self.npc_type)

    def __unicode__(self):
        return 'HP:{0}-Attack:{1}-Type:{2}'.format(self.hp, self.attack, self.npc_type)


class NPCShop(models.Model):
    price = models.IntegerField()
    npc_avatar = models.OneToOneField(NPCAvatar, on_delete=models.CASCADE)


class NPC(models.Model):
    pos_X = models.IntegerField()
    pos_Y = models.IntegerField()
    #Mapping
    npc_avatar = models.ForeignKey(NPCAvatar, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)

    def __str__(self):
        return 'NPC:{0}-World:({1})'.format(self.id, str(self.world))

    def __unicode__(self):
        return 'NPC:{0}-World:({1})'.format(self.id, str(self.world))
    


class User_NPC(models.Model):
    """
    Table to keep track history whether user has defeated the NPC or not
    TODO: When update this table, check and update User_World is_finished
    """
    is_defeated = models.BooleanField()
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    npc = models.ForeignKey(NPC, on_delete=models.CASCADE)


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


# User Customize

class CustomWorld(models.Model):
    description = models.CharField(max_length=255)
    background_type = models.IntegerField()
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CustomNPC(models.Model):
    pos_X = models.IntegerField()
    pos_Y = models.IntegerField()
    # Mapping
    npc_avatar = models.ForeignKey(NPCAvatar, on_delete=models.CASCADE)
    custom_world = models.ForeignKey(CustomWorld, on_delete=models.CASCADE)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)



