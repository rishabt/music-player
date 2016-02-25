# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0004_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.PositiveIntegerField(max_length=12)),
                ('songs_added', models.PositiveIntegerField(max_length=3)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
    ]
