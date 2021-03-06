# Generated by Django 3.0.5 on 2020-04-27 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('post_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VocabWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('definition', models.CharField(max_length=250)),
                ('audioClip', models.FileField(upload_to='vocab/audio/')),
                ('vocabList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.VocabList')),
            ],
        ),
        migrations.CreateModel(
            name='CheckOff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vocabWord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.VocabWord')),
            ],
        ),
    ]
