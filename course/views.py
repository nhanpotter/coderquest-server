from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

from .models import QuestionBank
from .serializers import *

class QuestionBankView(APIView):
    def get_object(self, pk):
        try: 
            return QuestionBank.objects.get(pk=pk)
        except QuestionBank.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bank = self.get_object(pk)
        serializer = QuestionBankSerializer(bank)

        return Response(serializer.data)


class OwnQuestionBankListView(APIView):
    def get(self, request, format=None):
        bank = QuestionBank.objects.filter(user=request.user)
        serializer = QuestionBankSerializer(many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionBankCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OwnQuestionBankUpdateDeleteView(APIView):
    def get_object(self, pk, user):
        try: 
            return QuestionBank.objects.get(pk=pk, user=user)
        except QuestionBank.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        bank = self.get_object(pk, request.user)
        serializer = QuestionBankCreateUpdateSerializer(bank, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        bank = self.get_object(pk, request.user)
        bank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OwnQuestionListView(APIView):
    def get(self, request, format=None):
        object_list = OwnQuestionList.objects.filter(user=request.user)
        questions = list(map(lambda obj: obj.question, object_list))

        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddQuestionSerializer(data=request.data)
        if serializer.is_valid():
            questions = serializer.validated_data['questions']
            for question in questions:
                OwnQuestionList.objects.create(user=request.user, question=question)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)