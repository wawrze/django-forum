# Generated by Django 3.0.4 on 2020-05-13 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0013_auto_20200513_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='id',
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]