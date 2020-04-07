from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer

from .models import *

User = get_user_model()

class ActiveUserSerializer(UserSerializer):
    first_time_login = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_active', 'first_time_login')

    def get_first_time_login(self, obj):
        return not hasattr(obj, 'avatar')


class AvatarSerializer(serializers.ModelSerializer):
    gender = serializers.IntegerField(min_value=1, max_value=2, required=False)

    class Meta:
        model = Avatar
        fields = '__all__'
        extra_kwargs = {
            'level': {'required': False},
            'experience': {'required': False},
            'gold': {'required': False},
            'hp': {'required': False},
            'attack': {'required': False},
            'clan': {'read_only': True},
            'user': {'read_only': True},
            'clan_owner': {'read_only': True}
        }

    def create(self, validated_data):
        return Avatar.objects.create(
            gender=validated_data['gender'],
            user=validated_data['user']
        )

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.gold = validated_data.get('gold', instance.gold)
        instance.hp = validated_data.get('hp', instance.hp)
        instance.attack = validated_data.get('attack', instance.attack)
        instance.save()
        return instance