# Generated by Django 3.0.5 on 2020-04-27 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabword',
            name='audioClip',
            field=models.FileField(null=True, upload_to='vocab/audio/'),
        ),
    ]
