# Generated by Django 3.0.5 on 2020-04-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_auto_20200409_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=-1),
        ),
    ]