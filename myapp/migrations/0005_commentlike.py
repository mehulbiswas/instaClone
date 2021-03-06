# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_commentmodel_likemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.CommentModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserModel')),
            ],
        ),
    ]
