# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-18 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
