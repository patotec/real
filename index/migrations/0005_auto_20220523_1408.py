# Generated by Django 2.2 on 2022-05-23 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20220523_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='category',
            field=models.CharField(choices=[('Rent', 'Rent'), ('Sale', 'Sell')], max_length=10, null=True),
        ),
    ]
