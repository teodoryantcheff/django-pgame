# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0032_auto_20150402_0302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blockprocessinghistory',
            options={'get_latest_by': 'timestamp', 'verbose_name_plural': 'BlockProcessingHistory'},
        ),
    ]
