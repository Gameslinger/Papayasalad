# Generated by Django 3.0.5 on 2020-04-27 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0012_resource_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
