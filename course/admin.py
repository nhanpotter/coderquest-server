from django.contrib import admin
from django.apps import apps
from .models import Course, Section, QuestionBank, Question
# Register your models here.

admin.site.register(Course)
admin.site.register(Section)

class OwnQuestionInline(admin.TabularInline):
    model = Question.user_list.through
    extra = 1
# Note: OwnQuestionInline is added to UserAdmin in app 'game'

class BankInline(admin.TabularInline):
    model = QuestionBank.questions.through
    extra = 1

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    inlines = (BankInline,)
    exclude = ('question_list',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (OwnQuestionInline,)
    exclude = ('user_list',)

