# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0036_auto_20150403_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ref_campaign',
            field=models.CharField(default=b'', max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ref_source',
            field=models.CharField(default=b'', max_length=64, null=True),
            preserve_default=True,
        ),
    ]
