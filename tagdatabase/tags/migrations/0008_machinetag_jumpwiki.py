# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0007_machinetag_wikilink'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetag',
            name='jumpWiki',
            field=models.BooleanField(default=False),
        ),
    ]
