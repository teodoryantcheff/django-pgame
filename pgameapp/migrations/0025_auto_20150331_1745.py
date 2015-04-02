# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0024_auto_20150331_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cryptotransaction',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp'},
        ),
        migrations.RenameField(
            model_name='cryptotransaction',
            old_name='game_currency',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='cryptotransaction',
            name='crypto_currency',
        ),
        migrations.RemoveField(
            model_name='cryptotransaction',
            name='user',
        ),
    ]
