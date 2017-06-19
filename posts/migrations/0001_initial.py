# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 14:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('post_date', models.DateField()),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RunPost',
            fields=[
                ('teampost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.TeamPost')),
                ('distance', models.FloatField()),
                ('duration', models.IntegerField()),
                ('route', models.CharField(max_length=64)),
            ],
            bases=('posts.teampost',),
        ),
        migrations.AddField(
            model_name='teampost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
