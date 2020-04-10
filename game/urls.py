from django.urls import path, include

from .views import *

urlpatterns = [
    path('expedition/', ExpeditionListView.as_view(), name='lobby'),
    path('expedition/<expedition_id>/', WorldListView.as_view(), name='expedition'),
    path('world/<world_id>/', WorldView.as_view(), name='world'),
    path('npc/<npc_id>/', NPCView.as_view(), name='npc-view'),
    path('npc/<npc_id>/defeat/', NPCDefeatView.as_view(), name='npc-defeat'),
]
