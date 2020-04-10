from django.utils import timezone
from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import *
from course.models import Question

class HistorySerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects)
    choice = serializers.IntegerField(min_value=1, max_value=4)

    def create(self, validated_data):
        validated_data['time'] = timezone.now()
        created = History(**validated_data)
        created.save()
        return created