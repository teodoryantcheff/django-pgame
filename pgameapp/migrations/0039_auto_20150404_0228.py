# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0038_auto_20150403_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actorprocurementhistory',
            name='actor',
        ),
        migrations.RemoveField(
            model_name='actorprocurementhistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='ActorProcurementHistory',
        ),
        migrations.RemoveField(
            model_name='coinconversionhistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='CoinConversionHistory',
        ),
        migrations.AlterModelOptions(
            name='userledger',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AlterField(
            model_name='actor',
            name='num_as_bonus',
            field=models.PositiveIntegerField(default=0, verbose_name=b'give as bonus'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actor',
            name='output',
            field=models.DecimalField(default=0, verbose_name=b'output / h (GC)', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actor',
            name='price',
            field=models.DecimalField(default=0, verbose_name=b'price (GC)', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referralbonuspayment',
            name='amount',
            field=models.DecimalField(verbose_name=b'bonus received', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referralbonuspayment',
            name='referred_user',
            field=models.ForeignKey(related_name='ref_payments', verbose_name=b'payer', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='type',
            field=models.CharField(max_length=10, choices=[(b'pmt', b'payment'), (b'b_rp', b'referral bonus'), (b'b_fp', b'1st payment bonus'), (b'wdr', b'withdrawal'), (b'bac', b'buy actor'), (b'w2i', b'w2i'), (b'sco', b'sell coins')]),
            preserve_default=True,
        ),
    ]
