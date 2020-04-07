from django.contrib.auth.models import User, Group
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TestingView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        content = {
            'connection': True
        }
        return Response(content)
