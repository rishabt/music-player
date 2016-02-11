# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=44)),
                ('add_time', models.DateTimeField(verbose_name='time song was added')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music_app.Room')),
            ],
        ),
    ]
