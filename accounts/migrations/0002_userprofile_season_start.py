# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 23:39
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='season_start',
            field=models.DateField(default=accounts.models._default_season_start),
        ),
    ]
