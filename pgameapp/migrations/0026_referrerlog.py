# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgameapp', '0025_auto_20150331_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferrerLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(verbose_name=b'Deposited real crypto', max_digits=16, decimal_places=5)),
                ('ref_source', models.CharField(default=b'', max_length=64, blank=True)),
                ('ref_campaign', models.CharField(default=b'', max_length=64, blank=True)),
                ('referred_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
