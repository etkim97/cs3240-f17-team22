# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_message_decrypted_msg_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='decrypted_msg_file',
            field=models.FileField(blank=True, upload_to='decrypted_messages'),
        ),
    ]