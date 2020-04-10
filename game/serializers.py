from rest_framework import serializers

from .models import *
from course.serializers import CourseSerializer, SectionSerializer, QuestionBankSerializer

class ExpeditionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Expedition
        fields = '__all__'


class WorldSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    is_finished = serializers.SerializerMethodField()

    class Meta:
        model = World
        exclude = ['user_history']

    def get_is_finished(self, obj):
        user = self.context['request'].user
        history = User_World.objects.get(user=user, world=obj)

        return history.is_finished


class NPCAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPCAvatar
        fields = '__all__'


class NPCSerializer(serializers.ModelSerializer):
    npc_avatar = NPCAvatarSerializer()
    is_defeated = serializers.SerializerMethodField()

    class Meta:
        model = NPC
        exclude = ['user_history']

    def get_is_defeated(self, obj):
        user = self.context['request'].user
        history = User_NPC.objects.get(user=user, npc=obj)

        return history.is_defeated

class NPCDetailSerializer(serializers.ModelSerializer):
    npc_avatar = NPCAvatarSerializer()
    question_bank = QuestionBankSerializer(read_only=True)
    is_defeated = serializers.SerializerMethodField()

    class Meta:
        model = NPC
        exclude = ['user_history']

    def get_is_defeated(self, obj):
        user = self.context['request'].user
        history = User_NPC.objects.get(user=user, npc=obj)

        return history.is_defeated


