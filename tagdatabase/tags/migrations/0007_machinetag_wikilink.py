# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0006_auto_20151204_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetag',
            name='wikiLink',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
