# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 07:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_commentmodel_upvote_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentmodel',
            name='UpVote_num',
        ),
    ]
