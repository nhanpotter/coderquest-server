from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['options'] = []
        ret['options'].append({
            'description': ret.pop('option1'),
            'option': 1,
        })
        ret['options'].append({
            'description': ret.pop('option2'),
            'option': 2,
        })
        ret['options'].append({
            'description': ret.pop('option3'),
            'option': 3,
        })
        ret['options'].append({
            'description': ret.pop('option4'),
            'option': 4,
        })
        return ret



class AddQuestionSerializer(serializers.Serializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Question.objects)


class QuestionBankSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionBank
        fields = '__all__'

class QuestionBankCreateUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Question.objects)

    class Meta:
        model = QuestionBank
        fields = '__all__'
        
