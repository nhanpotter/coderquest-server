from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

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