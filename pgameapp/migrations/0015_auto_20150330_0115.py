# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgameapp', '0014_auto_20150330_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('crypto_currency', models.DecimalField(verbose_name=b'Real money', max_digits=16, decimal_places=5)),
                ('game_currency', models.DecimalField(max_digits=16, decimal_places=5)),
                ('txid', models.CharField(max_length=128)),
                ('tx_type', models.CharField(max_length=1, choices=[(b'S', b'send'), (b'R', b'receive'), (b'M', b'move'), (b'O', b'orphan'), (b'I', b'immature'), (b'G', b'generate')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'get_latest_by': 'timestamp',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='cryptotransactionshistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='CryptoTransactionsHistory',
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 22, 15, 40, 509000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
