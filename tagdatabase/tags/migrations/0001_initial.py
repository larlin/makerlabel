# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('member_number', models.IntegerField(default=0)),
                ('box_num', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberBaseTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('print_date', models.DateField(verbose_name='print date')),
                ('comment', models.CharField(blank=True, max_length=50)),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberBoxTag',
            fields=[
                ('memberbasetag_ptr', models.OneToOneField(primary_key=True, to='tags.MemberBaseTag', auto_created=True, parent_link=True, serialize=False)),
                ('box_number', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('tags.memberbasetag',),
        ),
        migrations.CreateModel(
            name='MemberShelfTag',
            fields=[
                ('memberbasetag_ptr', models.OneToOneField(primary_key=True, to='tags.MemberBaseTag', auto_created=True, parent_link=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('tags.memberbasetag',),
        ),
        migrations.AddField(
            model_name='memberbasetag',
            name='member_id',
            field=models.ForeignKey(to='tags.Member'),
            preserve_default=True,
        ),
    ]
