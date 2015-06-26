# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0005_auto_20150623_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_number',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
