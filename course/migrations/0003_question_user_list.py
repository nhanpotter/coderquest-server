# Generated by Django 2.2 on 2020-04-09 15:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_ownquestionlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='user_list',
            field=models.ManyToManyField(related_name='question_list', to=settings.AUTH_USER_MODEL),
        ),
    ]