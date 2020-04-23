from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from djoser.utils import encode_uid

from .models import Avatar
User = get_user_model()

# Create your tests here.
class SignUpTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='feeder', password='dummy123',
            email='feeder@example.com', is_active=True
        )

    def test_sign_up_successfully(self):
        """
        Ensure user can sign up successfully through API
        """
        url = '/auth/users/'
        data = {
            'username': 'feeder_dev',
            'email': 'feeder_dev@example.com',
            'password': 'dummy123',
            're_password': 'dummy123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            user = User.objects.get(username='feeder_dev')
            self.assertEqual(user.username, 'feeder_dev')
            self.assertEqual(user.is_active, False)
        except User.DoesNotExist:
            self.assertTrue(False, "User Does Not Exists")

    def test_sign_up_existing_username(self):
        """
        User try to sign up with existing username
        """
        url = '/auth/users/'
        data = {
            'username': 'feeder',
            'email': 'feeder_dev@example.com',
            'password': 'dummy123',
            're_password': 'dummy123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_reply = response.json()
        self.assertEqual('username' in json_reply, True)

    def test_sign_up_invalid_email(self):
        """
        User input invalid email
        """
        url = '/auth/users/'
        data = {
            'username': 'feeder_dev',
            'email': 'feeder_dev',
            'password': 'dummy123',
            're_password': 'dummy123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_reply = response.json()
        self.assertEqual('email' in json_reply, True)

    def test_sign_up_invalid_password(self):
        """
        User's password does not match the requirements:
            "Password must not be similar to the username.",
            "It must contain at least 8 characters.",
            "This password must not be too common.",
            "This password must not be entirely numeric."
        """
        url = '/auth/users/'
        data = {
            'username': 'feeder_dev',
            'email': 'feeder_dev@example.com',
            'password': '123',
            're_password': '123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_reply = response.json()
        self.assertEqual('password' in json_reply, True)

    def test_sign_up_inconsistent_password(self):
        """
        User input different password and re_password in post data
        """
        url = '/auth/users/'
        data = {
            'username': 'feeder_dev',
            'email': 'feeder_dev@example.com',
            'password': 'dummy123',
            're_password': '123dummy',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_reply = response.json()
        self.assertEqual('non_field_errors' in json_reply, True)


class ActivationTestCase(APITestCase):
    def setUp(self):
        url = '/auth/users/'
        data = {
            'username': 'feeder',
            'email': 'feeder@example.com',
            'password': 'dummy123',
            're_password': 'dummy123',
        }
        response = self.client.post(url, data, format='json')

    def test_activation_link(self):
        """
        User Activate his account after sign up. The user must use the activation link that is sent
        to his email.
        """
        user = User.objects.get(username='feeder')
        uid = encode_uid(user.pk)
        token = default_token_generator.make_token(user)

        url = '/auth/users/activation/'
        data = {
            'uid': uid,
            'token': token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user.refresh_from_db()
        self.assertTrue(user.is_active)


class LoginTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='feeder', password='dummy123',
            email='feeder@example.com', is_active=True
        )

    def test_login_successfully(self):
        """
        Ensure user can login his activated account
        """
        url = '/auth/token/login/'
        data = {
            'username': 'feeder',
            'password': 'dummy123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            user = User.objects.get(username='feeder')
            token = Token.objects.get(user=user)
        except:
            self.assertTrue(False, "Token is not found")


    def test_login_failed(self):
        """
        User try to login with invalid credentials
        """
        url = '/auth/token/login/'
        data = {
            'username': 'feeder',
            'password': 'dummy'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class LogoutTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='feeder', password='dummy123',
            email='feeder@example.com', is_active=True
        )
        url = '/auth/token/login/'
        data = {
            'username': 'feeder',
            'password': 'dummy123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_logout(self):
        """
        Ensure user can log out
        """
        # User is currently logged in
        self.assertTrue(Token.objects.filter(user__username='feeder').exists())

        url = '/auth/token/logout/'
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Token.objects.filter(user__username='feeder').exists())

        
class CreateAvatarTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='feeder', password='dummy123',
            email='feeder@example.com', is_active=True
        )
        self.client.force_authenticate(user=self.user)

    def test_first_time_login(self):
        """
        For first-time-login user, when they check the user's info, the first-time-login flag 
        must be set to True, and avatar info has not been created yet
        """
        url = '/auth/users/me/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_reply = response.json()
        self.assertTrue(json_reply.get('first_time_login'))
        
        self.assertFalse(hasattr(self.user, 'avatar'))

    def test_create_avatar_successfully(self):
        """
        For first-time-login user, when they send their gender info through post request, system
        will automatically create an Avatar attached to the user
        """
        url = '/account/avatar/'

        # 1 is male, 2 is femal
        data = {
            'gender': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            self.assertTrue(Avatar.objects.get(user=self.user))
        except Avatar.DoesNotExist:
            self.assertTrue(False, 'Avatar is not created')
