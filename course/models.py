from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinValueValidator

# Create your models here.
from django.contrib.auth import get_user_model

import json
# Create your models here.

User = get_user_model()

class Course(models.Model):
    course_code = models.CharField(max_length=255, primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return 'Code:{0}-Name:{1}'.format(self.course_code, self.course_name)

    def __unicode__(self):
        return 'Code:{0}-Name:{1}'.format(self.course_code, self.course_name)


class Section(models.Model):
    # Mapping
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    level = models.IntegerField(validators=[MinValueValidator(1)])
    topic = models.CharField(max_length=255)
    description = models.TextField()


    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['level', 'course'],
                name='unique_level_for_course',
            )
        ]

    def __str__(self):
        return '{0}-Lv:{1}-Topic:{2}'.format(self.course.course_code, self.level, self.topic)

    def __unicode__(self):
        return '{0}-Lv:{1}-Topic:{2}'.format(self.course.course_code, self.level, self.topic)

    def get_questions(self):
        return self.question_set.all()

    def get_questions_sorted_by_difficulty(self):
        return self.get_questions().order_by('difficulty')
    

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Average'),
        (4, 'Hard'),
        (5, 'Very Hard')
    ]

    ANSWER_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    ]

    name = models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    # Question-related
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    answer = models.IntegerField(choices=ANSWER_CHOICES)

    # Mapping
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    user_list = models.ManyToManyField(User, related_name='question_list', blank=True)

    def __str__(self):
        return 'Sect:({1})-ID:{0}-Question:{2}'.format(self.id, str(self.section), self.name)

    def __unicode__(self):
        return 'Sect:({1})-ID:{0}-Question:{2}'.format(self.id, str(self.section), self.name)

    def get_difficulty_string(self):
        return Question.DIFFICULTY_CHOICES[self.difficulty-1][1]

    def get_correct_percentage(self):
        history_list = self.history_set.all()

        if len(history_list) == 0:
            return "No Attempt Recorded"
        
        correct_list = history_list.filter(correct=True)
        return str(round(len(correct_list) / len(history_list) * 100, 2)) + "%"



class QuestionBank(models.Model):
    name = models.CharField(max_length=255)
    # Mapping
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name='question_bank_list')

    def __str__(self):
        return 'ID:{0}-Name:{1}'.format(self.id, self.name)

    def __unicode__(self):
        return 'ID:{0}-Name:{1}'.format(self.id, self.name)



