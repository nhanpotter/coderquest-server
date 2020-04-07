from django.contrib import admin
from django.apps import apps

# Register your models here.
model_list = apps.get_app_config('game').get_models()

for model in model_list:
    admin.site.register(model)