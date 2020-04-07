from django.db import models
from django.contrib.auth import get_user_model

from course.models import Question

User = get_user_model()

# Create your models here.
class History(models.Model):
    time = models.DateTimeField()
    choice = models.IntegerField(choices=Question.ANSWER_CHOICES)

    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)