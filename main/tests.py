from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

import time

User = get_user_model()
# Create your tests here.

class LoadTestcase(APITestCase):
    # Number of user to test
    number = 1

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        number = LoadTestcase.number

        start_time = time.time()
        for i in range(1000, 1000+ number):
            username = 'user'+str(i)
            User.objects.create_user(username=username, password=str(i), is_active=True)
        print('---Time taken to create {0} user(s): {1} seconds ---'.format(
            number, time.time() - start_time
        ))


    def test_load_user_login(self):
        number = LoadTestcase.number

        url = '/auth/token/login/'
        start_time = time.time()
        for i in range(1000,1000+number):
            username = 'user'+str(i)
            data = {
                'username': username,
                'password': str(i)
            }
            self.client.post(url, data, format='json')
        print("---Time taken for {0} user(s) to login: {1} seconds ---".format(
            number, time.time() - start_time
        ))

    def test_load_user_logout(self):
        number = LoadTestcase.number

        url = '/auth/token/logout/'
        start_time = time.time()
        for i in range(1000, 100+number):
            username = 'user'+str(i)
            user = User.objects.get(username=username)
            self.client.force_authenticate(user=user)
            self.client.post(url, {}, format='json')
        print("---Time taken for {0} user(s) to log out: {1} seconds ---".format(
            number, time.time() - start_time
        ))


            
