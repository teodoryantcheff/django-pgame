# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0028_auto_20150402_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='referrerlog',
            name='ref_campaign',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='referrerlog',
            name='ref_source',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
