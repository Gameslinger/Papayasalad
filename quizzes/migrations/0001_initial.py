# Generated by Django 3.0.5 on 2020-04-09 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('response_type', models.CharField(choices=[('TF', 'Text Field'), ('RB', 'Radio Button')], default='TF', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RadioResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.Question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='Quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.Quiz'),
        ),
    ]