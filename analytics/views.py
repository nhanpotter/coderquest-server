from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import *
from game.models import Expedition, World

User = get_user_model()

class SendHistoryView(APIView):
    def post(self, request, format=None):
        serializer = HistorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/admin/login/')
def data_analysis_home(request):
    expedition = Expedition.objects.first()

    if not expedition:
        return Http404("No Expedition Available")

    return HttpResponseRedirect(reverse('data-analysis', args=(expedition.id,)))


@login_required(login_url='/admin/login/')
def data_analysis(request, expedition_id):
    kwargs = {}

    try:
        expedition = Expedition.objects.get(id=expedition_id)
    except Expedition.DoesNotExist:
        return Http404("This expedition does not exists")

    # Header Preparation
    kwargs['users'] = len(User.objects.filter(is_staff=False))
    kwargs['active_users'] = len(Token.objects.filter(user__is_staff=False))
    kwargs['finished'] = expedition.get_number_students_finished()
    kwargs['complete'] = expedition.get_complete_percentage()
    kwargs['correct'] = expedition.get_correct_percentage()

    expedition_list = Expedition.objects.all()
    kwargs['expedition'] = expedition
    kwargs['world_list'] = expedition.world_set.order_by('section__level')
    kwargs['world_id_list'] = []
    for world in kwargs['world_list']:
        kwargs['world_id_list'].append(world.get_html_id())
    kwargs['expedition_list'] = expedition_list

    return render(request, 'analytics/index.html', kwargs)