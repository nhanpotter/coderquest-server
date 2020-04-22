from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Social)
# admin.site.register(Clan)
admin.site.register(Avatar)

class AvatarInline(admin.TabularInline):
    model = Avatar
# Note: AvatarInline is added to UserAdmin in app 'game'