# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0006_member_member_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='comment',
            field=models.CharField(blank=True, max_length=50),
            preserve_default=True,
        ),
    ]
