from django.shortcuts import render
from django.http import HttpResponse
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from requests_oauthlib import OAuth2Session
from server.settings import AUTH_API_URL
from .serializers import AvatarSerializer

# Create your views here.
# Activation
def account_activate(request, uid, token):
    url = AUTH_API_URL + '/users/activation/'
    kwargs = {
        'uid': uid,
        'token': token,
    }
    post_request = requests.post(url, data=kwargs)

    return HttpResponse('Activation Successful')


class AvatarView(APIView):
    def get(self, request, format=None):
        if hasattr(request.user, 'avatar'):
            serializer = AvatarSerializer(request.user.avatar)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Avatar Not Exist'},
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
                    {'error': 'Gender field is not provided, Avatar not created'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(user=request.user)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GoogleOAuth2(APIView):
#     """
#     Login with Google OAuth2
#     """

#     def get(self, request):
#         client_id = settings.GOOGLE_OAUTH2_KEY
#         scope = settings.GOOGLE_OAUTH2_SCOPE
#         redirect_uri = request.query_params.get('redirect_uri')
#         if redirect_uri not in settings.SOCIAL_AUTH_ALLOWED_REDIRECT_URIS:
#             return response.Response(
#                 {
#                     'error': 'Wrong Redirect URI'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
#         authorization_url, state = google.authorization_url(
#             settings.GOOGLE_AUTHORIZATION_BASE_URL,
#             access_type='offline',
#             prompt='select_account'
#         )
#         return response.Response({'authorization_url': authorization_url})

#     def post(self, request):

#         client_id = settings.GOOGLE_OAUTH2_KEY
#         client_secret = settings.GOOGLE_OAUTH2_SECRET

#         state = request.data.get('state')
#         code = request.data.get('code')
#         redirect_uri = request.data.get('redirect_uri')

#         google = OAuth2Session(
#             client_id,
#             redirect_uri=redirect_uri,
#             state=state
#         )
#         google.fetch_token(
#             settings.GOOGLE_TOKEN_URL,
#             client_secret=client_secret,
#             code=code
#         )

#         user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
#         user_email = user_info['email']
#         try:
#             user = User.objects.get(email=user_email)
#         except User.DoesNotExist:
#             # Decide if you want to create a new user
#             user = User.objects.create_user()
#         refresh_token = RefreshToken.for_user(user)
#         return response.Response({
#             'refresh': str(refresh_token),
#             'access': str(refresh_token.access_token)
#         })