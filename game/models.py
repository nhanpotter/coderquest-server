from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from course.models import Course, Section, QuestionBank
from analytics.models import History
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

    def get_number_students_finished(self):
        user_list = User.objects.filter(is_staff=False)
        count = 0
        for user in user_list:
            unfinished = User_World.objects.filter(
                user=user, world__expedition=self, is_finished=False
            )
            if not unfinished.exists():
                count += 1

        return count

    def get_complete_percentage(self):
        history = User_World.objects.all()
        if not history.exists():
            return "N.A"

        unfinished = history.filter(
            world__expedition=self, is_finished=False
        )

        percentage = round((1-len(unfinished)/len(history))*100,2)
        return str(percentage)+"%"

    def get_correct_percentage(self):
        history = History.objects.filter(question__section__course=self.course)
        if not history.exists():
            return "N.A"

        correct = history.filter(correct=True)

        percentage = round(len(correct)/len(history)*100,2)
        return str(percentage)+"%"

class World(models.Model):
    BACKGROUND_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
    ]
    # Mapping
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE)
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    user_history = models.ManyToManyField(
        User, 
        through='game.User_World',
        through_fields=('world', 'user'),
        related_name='world_history',
    )

    # Attribute
    background_type = models.IntegerField(choices=BACKGROUND_CHOICES)   


    def __str__(self):
        return 'Expedition:({0}) Section:({1})'.format(str(self.expedition), str(self.section))

    def __unicode__(self):
        return 'Expedition:({0}) Section:({1})'.format(str(self.expedition), str(self.section))

    def get_html_id(self):
        return "world-{}".format(self.id)

    def get_html_id_portion(self):
        return "world-{}-portion".format(self.id)

    def get_html_id_correct(self):
        return "world-{}-correct".format(self.id)

    def get_npcs(self):
        return self.npc_set.all()

    npcs = property(get_npcs)

    def get_questions_sorted_by_difficulty(self):
        return self.section.get_questions_sorted_by_difficulty()

    def get_student_portion(self):
        history = User_World.objects.filter(world=self)
        undone_list = history.filter(is_finished=False)
        
        doing_number = 0
        for item in undone_list:
            if User_NPC.objects.filter(user=item.user, npc__world=self, is_defeated=True).exists():
                doing_number += 1

        total = len(history)
        done_number = total - len(undone_list)
        not_started_number = total - done_number - doing_number
        return {
            'done': done_number,
            'doing': doing_number,
            'not': not_started_number,
        }

    def get_correct_percentage(self):
        history = History.objects.filter(question__section=self.section)
        if not history.exists():
            return {
                'correct': 0,
                'incorrect': 100,
            }

        correct_list = history.filter(correct=True)

        correct = round(len(correct_list)/len(history) * 100, 2)
        incorrect = round(100-correct, 2)
        return {
            'correct': correct,
            'incorrect': incorrect,
        }


class User_World(models.Model):
    """
    Table to keep track history whether user has finished the world or not
    """
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    #Attribute
    is_finished = models.BooleanField()



class NPCAvatar(models.Model):
    NPC_CHOICES = [(i+1,i+1) for i in range(5)]

    hp = models.IntegerField()
    attack = models.IntegerField()
    npc_type = models.IntegerField(choices=NPC_CHOICES)

    def __str__(self):
        return 'HP:{0}-Attack:{1}-Type:{2}'.format(self.hp, self.attack, self.npc_type)

    def __unicode__(self):
        return 'HP:{0}-Attack:{1}-Type:{2}'.format(self.hp, self.attack, self.npc_type)


class NPCShop(models.Model):
    price = models.IntegerField()
    npc_avatar = models.OneToOneField(NPCAvatar, on_delete=models.CASCADE)


class NPC(models.Model):
    pos_X = models.DecimalField(
        max_digits=4, 
        decimal_places=3,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ]
    )
    pos_Y = models.DecimalField(
        max_digits=4, 
        decimal_places=3,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ]
    )
    boss = models.BooleanField(default=False)
    experience = models.IntegerField()
    gold = models.IntegerField()
    #Mapping
    npc_avatar = models.ForeignKey(NPCAvatar, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    user_history = models.ManyToManyField(
        User,
        through='game.User_NPC',
        through_fields=('npc', 'user'),
        related_name='npc_history',
    )

    def __str__(self):
        return 'NPC:{0}-World:({1})'.format(self.id, str(self.world))

    def __unicode__(self):
        return 'NPC:{0}-World:({1})'.format(self.id, str(self.world))
    


class User_NPC(models.Model):
    """
    Table to keep track history whether user has defeated the NPC or not
    TODO: When update this table, check and update User_World is_finished
    """
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    npc = models.ForeignKey(NPC, on_delete=models.CASCADE)

    # Attribute
    is_defeated = models.BooleanField()


# User Customize

class CustomWorld(models.Model):
    description = models.CharField(max_length=255)
    background_type = models.IntegerField(choices=World.BACKGROUND_CHOICES)
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CustomNPC(models.Model):
    pos_X = models.IntegerField()
    pos_Y = models.IntegerField()
    # Mapping
    npc_avatar = models.ForeignKey(NPCAvatar, on_delete=models.CASCADE)
    custom_world = models.ForeignKey(CustomWorld, on_delete=models.CASCADE)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)



