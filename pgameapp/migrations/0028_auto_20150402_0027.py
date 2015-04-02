# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0027_auto_20150401_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cryptotransaction',
            old_name='crypto_address',
            new_name='address',
        ),
        migrations.AlterField(
            model_name='referrerlog',
            name='amount',
            field=models.DecimalField(verbose_name=b'credit', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
    ]
