from django.shortcuts import render
from django.http import Http404
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

class ExpeditionListView(APIView):
    def get(self, request, format=None):
        expeditions = Expedition.objects.all()
        serializer = ExpeditionSerializer(expeditions, many=True)

        return Response(serializer.data)


class WorldListView(APIView):
    def get(self, request, expedition_id, format=None):
        worlds = World.objects.filter(expedition__id=expedition_id)
        worlds = worlds.order_by('section__level')
        serializer = WorldSerializer(worlds, many=True, context={'request': request})

        return Response(serializer.data)


class WorldView(APIView):
    def get(self, request, world_id, format=None):
        npcs = NPC.objects.filter(world__id=world_id)
        serializer = NPCSerializer(npcs, many=True, context={'request': request})

        return Response(serializer.data)


class NPCView(APIView):
    def get_object(self, pk):
        try:
            return NPC.objects.get(pk=pk)
        except NPC.DoesNotExist:
            raise Http404

    def get(self, request, npc_id, format=None):
        npc = self.get_object(npc_id)
        serializer = NPCDetailSerializer(npc, context={'request': request})

        return Response(serializer.data)


class NPCDefeatView(APIView):
    def get_object(self, pk):
        try:
            return NPC.objects.get(pk=pk)
        except NPC.DoesNotExist:
            raise Http404

    def post(self, request, npc_id, format=None):
        npc = self.get_object(npc_id)
        user = request.user
        history = User_NPC.objects.get(npc=npc, user=user)
        is_defeated = history.is_defeated

        if is_defeated:
            res = {
                'detail': 'This user already defeat this NPC',
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            history.is_defeated = True
            history.save()

            avatar = user.avatar
            avatar.experience += npc.experience
            avatar.gold += npc.gold
            avatar.save()

            return Response(status=status.HTTP_200_OK)
