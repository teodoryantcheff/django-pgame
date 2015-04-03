# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0035_auto_20150403_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralstats',
            name='referred_user',
            field=models.ForeignKey(related_name='hui', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
