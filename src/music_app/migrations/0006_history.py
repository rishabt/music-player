# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0005_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=44)),
                ('add_time', models.DateTimeField(verbose_name='time song was added')),
                ('room', models.ForeignKey(to='music_app.Room')),
            ],
        ),
    ]
