# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170619_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='runpost',
            name='details',
            field=models.TextField(default=''),
        ),
    ]