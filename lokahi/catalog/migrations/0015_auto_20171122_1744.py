# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 22:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_user_is_suspended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(default=1, max_length=10),
        ),
    ]