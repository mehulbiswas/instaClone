# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_remove_commentmodel_upvote_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_text', models.CharField(max_length=255)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.PostModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserModel')),
            ],
        ),
        migrations.CreateModel(
            name='clarifai_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clarifai_data', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserModel')),
            ],
        ),
    ]
