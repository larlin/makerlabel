# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberbasetag',
            name='visible',
        ),
        migrations.AddField(
            model_name='basetag',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
