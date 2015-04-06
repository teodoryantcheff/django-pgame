# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgameapp', '0042_auto_20150404_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawalrequest',
            name='user',
            field=models.ForeignKey(related_name='withdrawalrequest_related', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
