# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_auto_20151127_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetag',
            name='name',
            field=models.CharField(default='Test', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='machinetag',
            name='info',
            field=models.CharField(max_length=400, blank=True),
            preserve_default=True,
        ),
    ]
