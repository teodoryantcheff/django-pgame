# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgameapp', '0037_auto_20150403_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralBonusPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=16, decimal_places=5)),
                ('ref_source', models.CharField(default=b'', max_length=64, blank=True)),
                ('ref_campaign', models.CharField(default=b'', max_length=64, blank=True)),
                ('referred_user', models.ForeignKey(related_name='ref_payments', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='referralbonuspayment_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='referralstats',
            name='referred_user',
        ),
        migrations.RemoveField(
            model_name='referralstats',
            name='user',
        ),
        migrations.DeleteModel(
            name='ReferralStats',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ref_campaign',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ref_source',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
