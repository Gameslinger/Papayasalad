# Generated by Django 3.0.5 on 2020-04-17 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_auto_20200411_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correctAnswer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
