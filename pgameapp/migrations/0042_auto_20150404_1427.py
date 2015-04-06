# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0041_auto_20150404_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='decided_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
