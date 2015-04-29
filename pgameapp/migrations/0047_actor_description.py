# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0046_auto_20150407_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
