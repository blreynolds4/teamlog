# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_postcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['comment_timestamp']},
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='comment_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
