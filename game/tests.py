from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from account.models import Avatar
from .models import NPC, User_NPC, World, User_World

User = get_user_model()

class DefeatNPCTestCase(APITestCase):
    """
    Pre-load database fixtures with adequate expedition, world and NPC for testing. This fixture
    file contains data from the database. The files is generated using command
    *python manage.py dumpdata - exclude auth.permission - exclude contenttypes > data.json*
    """
    fixtures = ['data.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username='new_user', password='dummy123',
            email='new@example.com', is_active=True
        )
        self.client.force_authenticate(user=self.user)
        self.avatar = Avatar.objects.create(user=self.user, gender=1, level=1, experience=0, gold=0)
        self.npc = NPC.objects.first()
        self.npc.experience = 10
        self.npc.gold = 10
        self.npc.save()

    def test_npc_defeat_no_edge_case(self):
        """
        Ensure user defeat NPC and get is_defeated flag turns to True and get reward with same 
        amount that the NPC has. In this case, user will not leveled up
        """
        url = '/game/npc/{}/defeat/'.format(self.npc.id)
        user_npc = User_NPC.objects.get(user=self.user, npc=self.npc)
        self.assertFalse(user_npc.is_defeated, "Make sure user_npc is initially False ")

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user_npc.refresh_from_db()
        self.assertTrue(user_npc.is_defeated)

        self.avatar.refresh_from_db()
        new_exp = self.avatar.experience
        new_gold = self.avatar.gold

        self.assertEqual(new_exp, self.npc.experience)
        self.assertEqual(new_gold, self.npc.gold)

    def test_npc_defeat_edge_case(self):
        """
        Ensure user defeat NPC and get is_defeated flag turns to True and get reward with same 
        amount that the NPC has. In this case, user's experience will bypass 100 and user will be
        leveled up.
        """
        url = '/game/npc/{}/defeat/'.format(self.npc.id)
        user_npc = User_NPC.objects.get(user=self.user, npc=self.npc)
        self.assertFalse(user_npc.is_defeated, "Make sure user_npc is initially False ")

        old_exp = self.avatar.experience
        old_level = self.avatar.level

        # Turn NPC experience reward to 210
        self.npc.experience = 210
        self.npc.save()

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user_npc.refresh_from_db()
        self.assertTrue(user_npc.is_defeated)

        self.avatar.refresh_from_db()
        new_exp = self.avatar.experience
        new_level = self.avatar.level

        reward_count = 100 - old_exp
        old_level += 1

        while (old_level < new_level):
            reward_count += 100
            old_level += 1

        reward_count += new_exp

        self.assertEqual(reward_count, self.npc.experience)

    def test_all_npc_in_world_is_defeated(self):
        """
        Ensure when all NPC in a world is defeated, the flag is_finished for that world turns to
        True
        """
        world = World.objects.first()
        npc_set = world.npc_set.all()

        user_world = User_World.objects.get(user=self.user, world=world)
        self.assertFalse(user_world.is_finished)

        for npc in npc_set:
            url = '/game/npc/{}/defeat/'.format(npc.id)
            user_npc = User_NPC.objects.get(user=self.user, npc=npc)
            self.assertFalse(user_npc.is_defeated, "Make sure user_npc is initially False ")

            response = self.client.post(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_world.refresh_from_db()
        self.assertTrue(user_world.is_finished)