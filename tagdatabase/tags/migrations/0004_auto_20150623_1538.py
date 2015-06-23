# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_auto_20150623_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='print_date',
            field=models.DateField(verbose_name='print date'),
            preserve_default=True,
        ),
    ]
