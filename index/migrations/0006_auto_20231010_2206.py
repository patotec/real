# Generated by Django 2.2 on 2023-10-10 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20220523_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='photo_1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='photo_2',
        ),
        migrations.RemoveField(
            model_name='property',
            name='photo_3',
        ),
        migrations.RemoveField(
            model_name='property',
            name='photo_4',
        ),
        migrations.RemoveField(
            model_name='property',
            name='photo_5',
        ),
    ]
