from django.shortcuts import render
from django.http import HttpResponse
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from requests_oauthlib import OAuth2Session
from server.settings import BASE_SERVER_URL
from .serializers import AvatarSerializer
from .models import Avatar

# Create your views here.
# Activation
def account_activate(request, uid, token):
    url = BASE_SERVER_URL + 'auth/users/activation/'
    kwargs = {
        'uid': uid,
        'token': token,
    }
    requests.post(url, data=kwargs)

    return HttpResponse('Activation Successful')


class AvatarView(APIView):
    def get(self, request, format=None):
        if hasattr(request.user, 'avatar'):
            serializer = AvatarSerializer(request.user.avatar)
            return Response(serializer.data)
        else:
            return Response(
                {'detail': 'Avatar Not Exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, format=None):
        is_avatar_existed = hasattr(request.user, 'avatar')
        if is_avatar_existed:
            serializer = AvatarSerializer(request.user.avatar, data=request.data)
        else:
            serializer = AvatarSerializer(data=request.data)
        if serializer.is_valid():                
            if not is_avatar_existed and 'gender' not in serializer.validated_data:
                return Response(
                    {'detail': 'Gender field is not provided, Avatar not created'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(user=request.user)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardView(APIView):
    def get(self, request, format=None):
        avatar_list = Avatar.objects.order_by('-level', '-experience')
        serializer = AvatarSerializer(avatar_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)