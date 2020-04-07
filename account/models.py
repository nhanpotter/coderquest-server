from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Social(models.Model):
    facebook_ID = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + '-' + self.user.username

    def __unicode__(self):
        return str(self.id) + '-' + self.user.username

class Clan(models.Model):
    clan_name = models.CharField(max_length=255)
    max_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.id) + '-' + self.clan_name

    def __unicode__(self):
        return str(self.id) + '-' + self.clan_name

class Avatar(models.Model):
    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female')
    ]

    gender = models.IntegerField(choices=GENDER_CHOICES)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    hp = models.IntegerField(default=100)
    attack = models.IntegerField(default=10)
    # Mapping
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clan_owner = models.OneToOneField(
        Clan, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='clan_owner'
    )

    def __str__(self):
        return str(self.id) + '-' + self.user.username

    def __unicode__(self):
        return str(self.id) + '-' + self.user.username

    def clean(self):
        """
        Make sure if user is the owner of the clan, he is also the member of the clan
        """
        if clan_owner is not None:
            clan = clan_owner
            self.save()

