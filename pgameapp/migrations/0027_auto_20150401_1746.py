# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0026_referrerlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referrerlog',
            name='ref_campaign',
        ),
        migrations.RemoveField(
            model_name='referrerlog',
            name='ref_source',
        ),
    ]
