from django.urls import include, path

from .views import *

urlpatterns = [
    path('question_bank/detail/<pk>/', QuestionBankView.as_view(), name='Question Bank'),
    path('question_bank/me/', OwnQuestionBankListView.as_view(), name='Own Question Bank'),
    path('question_bank/me/<pk>/', OwnQuestionBankUpdateDeleteView.as_view(), name='Delete Upate Own Question Bank'),
    path('question/me/', OwnQuestionListView.as_view(), name='Own Question List'),
]
