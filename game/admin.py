from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.apps import apps
from django.utils.safestring import mark_safe

from .models import Expedition, World, User_World, NPC, NPCShop, NPCAvatar, User_NPC
from course.admin import OwnQuestionInline

User = get_user_model()

# Register your models here.
admin.site.register(NPCShop)
admin.site.register(NPCAvatar)

class WorldInline(admin.TabularInline):
    model = World
    extra = 1

@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    inlines = (WorldInline,)

class NPCInline(admin.TabularInline):
    model = NPC
    extra = 1

class User_WorldInline(admin.TabularInline):
    model = User_World
    extra = 1

@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    # list_display = ('__str__', 'show_image',)
    # readonly_fields = ('show_image',)
    inlines = (
        NPCInline,
        User_WorldInline,
    )

    # def show_image(self, instance):
    #     # url = "<a href=\"javascript:window.open('#', 'World ID {0}', 'width=800,height=450');\" >Show Image</a>".format(instance.id)
    #     # return mark_safe(url)\
    #     return type(instance)

class User_NPCInline(admin.TabularInline):
    model = User_NPC
    extra = 1

@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    inlines = (User_NPCInline,)

class UserAdmin(UserAdmin):
    inlines = (
        OwnQuestionInline,
        User_WorldInline,
        User_NPCInline,
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
