# Generated by Django 3.0.5 on 2020-04-07 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_teacher', models.BooleanField()),
                ('join_date', models.DateTimeField(verbose_name='join date')),
                ('last_logged_on', models.DateTimeField(verbose_name='last logged on date')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.Room')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]