from django.contrib import admin
from django.apps import apps
from .models import Course, Section, QuestionBank, Question
# Register your models here.

admin.site.register(Course)

class OwnQuestionInline(admin.TabularInline):
    model = Question.user_list.through
    extra = 1
# Note: OwnQuestionInline is added to UserAdmin in app 'game'


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)

class SectionListFilter(admin.SimpleListFilter):
    title = 'Section'

    parameter_name = 'section'

    def lookups(self, request, model_admin):
        get_data = request.GET
        course_code = get_data.get('section__course__course_code__exact')

        if course_code:
            course = Course.objects.get(course_code=course_code)
            section_set = course.section_set.all()
            return ((sect.pk, sect.__str__) for sect in section_set)

    def queryset(self, request, queryset):
        if self.value():
            section = Section.objects.get(pk=self.value())
            return queryset.filter(section=section)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (OwnQuestionInline,)
    exclude = ('user_list',)
    list_filter = ('section__course', SectionListFilter)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_filter = ('course',)
