# Generated by Django 3.0.5 on 2020-04-17 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0009_auto_20200417_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
