# Generated by Django 2.2 on 2020-04-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_delete_ownquestionlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionbank',
            name='question_list',
            field=models.ManyToManyField(related_name='question_bank_list', to='course.Question'),
        ),
        migrations.DeleteModel(
            name='QuestionBank_Question',
        ),
    ]
