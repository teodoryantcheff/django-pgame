# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0044_auto_20150404_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referralbonuspayment',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp'},
        ),
        migrations.AlterModelOptions(
            name='userledger',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp'},
        ),
        migrations.AlterModelOptions(
            name='withdrawalrequest',
            options={'ordering': ('-timestamp',), 'get_latest_by': 'timestamp'},
        ),
        migrations.AlterField(
            model_name='userledger',
            name='object_id1',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='object_id2',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='object_id3',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='object_type1',
            field=models.ForeignKey(related_name='log_items1', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='object_type2',
            field=models.ForeignKey(related_name='log_items2', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='object_type3',
            field=models.ForeignKey(related_name='log_items3', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='serialized_data',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
