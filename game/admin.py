from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.apps import apps
from django.utils.safestring import mark_safe

from .models import Expedition, World, User_World, NPC, NPCShop, NPCAvatar, User_NPC
from course.admin import OwnQuestionInline
from account.admin import AvatarInline

User = get_user_model()

# Register your models here.
# admin.site.register(NPCShop)
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
    list_filter = ('expedition',)
    inlines = (
        NPCInline,
        User_WorldInline,
    )


class User_NPCInline(admin.TabularInline):
    model = User_NPC
    extra = 1

class WorldListFilter(admin.SimpleListFilter):
    title = 'World'

    parameter_name = 'world'

    def lookups(self, request, model_admin):
        get_data = request.GET
        expedition_id = get_data.get('world__expedition__id__exact')

        if expedition_id:
            expedition = Expedition.objects.get(id=expedition_id)
            world_set = expedition.world_set.all()
            return ((world.pk, world.__str__) for world in world_set)

    def queryset(self, request, queryset):
        if self.value():
            world = World.objects.get(pk=self.value())
            return queryset.filter(world=world)


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_filter = ('world__expedition', WorldListFilter)
    inlines = (User_NPCInline,)

class UserAdmin(UserAdmin):
    inlines = (
        AvatarInline,
        OwnQuestionInline,
        User_WorldInline,
        User_NPCInline,
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
