# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0050_merge_20171204_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]