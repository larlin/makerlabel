# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_auto_20151127_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentTime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 11, 28, 12, 19, 35, 111348, tzinfo=utc), verbose_name='comment time'),
            preserve_default=False,
        ),
    ]
