# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('print_date', models.DateField(verbose_name='print date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineTag',
            fields=[
                ('basetag_ptr', models.OneToOneField(auto_created=True, serialize=False, to='tags.BaseTag', parent_link=True, primary_key=True)),
                ('info', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=('tags.basetag',),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
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
                ('basetag_ptr', models.OneToOneField(auto_created=True, serialize=False, to='tags.BaseTag', parent_link=True, primary_key=True)),
                ('comment', models.CharField(max_length=50, blank=True)),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=('tags.basetag',),
        ),
        migrations.CreateModel(
            name='MemberBoxTag',
            fields=[
                ('memberbasetag_ptr', models.OneToOneField(auto_created=True, serialize=False, to='tags.MemberBaseTag', parent_link=True, primary_key=True)),
                ('box_number', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=('tags.memberbasetag',),
        ),
        migrations.CreateModel(
            name='MemberShelfTag',
            fields=[
                ('memberbasetag_ptr', models.OneToOneField(auto_created=True, serialize=False, to='tags.MemberBaseTag', parent_link=True, primary_key=True)),
            ],
            options={
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
