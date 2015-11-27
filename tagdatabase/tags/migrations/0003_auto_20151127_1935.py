# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20151127_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('commentText', models.CharField(max_length=400)),
                ('machine', models.ForeignKey(to='tags.MachineTag')),
                ('writer', models.ForeignKey(to='tags.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='machinetag',
            name='contact',
            field=models.ForeignKey(to='tags.Member', default=1),
            preserve_default=False,
        ),
    ]
