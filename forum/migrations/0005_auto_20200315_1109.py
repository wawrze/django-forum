# Generated by Django 3.0.4 on 2020-03-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0004_auto_20200315_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateTimeField(),
        ),
    ]