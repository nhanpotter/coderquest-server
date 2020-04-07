from django.contrib import admin
from django.apps import apps
from .models import *
# Register your models here.

model_list = apps.get_app_config('course').get_models()

for model in model_list:
    admin.site.register(model)
