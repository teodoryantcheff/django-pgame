# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0043_withdrawalrequest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='status',
            field=models.CharField(default=b'P', max_length=1, choices=[(b'A', b'approved'), (b'P', b'pending'), (b'D', b'denied'), (b'$', b'paid')]),
            preserve_default=True,
        ),
    ]
