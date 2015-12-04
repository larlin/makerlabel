# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0005_comment_commenttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetag',
            name='dnh',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='machinetag',
            name='loan',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='machinetag',
            name='rtfm',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
