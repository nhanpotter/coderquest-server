# Generated by Django 2.2 on 2020-03-19 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200319_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatar',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1),
            preserve_default=False,
        ),
    ]
