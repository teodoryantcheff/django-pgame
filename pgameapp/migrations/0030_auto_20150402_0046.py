# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgameapp', '0029_auto_20150402_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(verbose_name=b'credit', max_digits=16, decimal_places=5)),
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
        migrations.RemoveField(
            model_name='referrerlog',
            name='referred_user',
        ),
        migrations.RemoveField(
            model_name='referrerlog',
            name='user',
        ),
        migrations.DeleteModel(
            name='ReferrerLog',
        ),
    ]
