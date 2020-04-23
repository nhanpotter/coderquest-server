from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from .models import History
from course.models import Question
import random

User = get_user_model()

class SendHistoryTestCase(APITestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username='new_user', password='dummy123',
            email='new@example.com', is_active=True
        )
        self.client.force_authenticate(user=self.user)

    def test_send_history(self):
        """
        Ensure user can send history of answers and these get saved in the database
        """
        questions = Question.objects.all()
        self.assertTrue(len(questions)>5)

        selected_questions = questions[:5]
        data = []
        for question in selected_questions:
            data.append({
                'question': question.id,
                'choice': random.randint(1,4)
            })

        url = '/analytics/send_history/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            for item in data:
                history = \
                    History.objects.filter(user=self.user, question__id=item['question']).first()
                self.assertEqual(history.choice, item['choice'])
        except:
            self.assertTrue(False, 'History object is not created properly')



