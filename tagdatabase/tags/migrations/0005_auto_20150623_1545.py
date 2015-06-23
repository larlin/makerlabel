# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_auto_20150623_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='user_id',
            new_name='member_id',
        ),
    ]
