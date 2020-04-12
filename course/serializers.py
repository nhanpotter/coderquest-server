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
        exclude = ['user_list']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['question_id'] = ret.pop('id')
        ret['a1'] = ret.pop('option1')
        ret['a2'] = ret.pop('option2')
        ret['a3'] = ret.pop('option3')
        ret['a4'] = ret.pop('option4')
        
        answer_str = 'a' + str(instance.answer)
        ret['answer'] = ret[answer_str]        
        
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
        
