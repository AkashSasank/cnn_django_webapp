# Generated by Django 3.0.2 on 2020-01-14 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='name',
        ),
    ]
