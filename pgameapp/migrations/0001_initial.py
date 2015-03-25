# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('custom_user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0)),
                ('output', models.FloatField(default=0)),
                ('image_path', models.CharField(max_length=50, null=True, verbose_name=b'actor image file location', blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['price'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActorProcurementHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField(verbose_name=b'Price of procurement')),
                ('actor', models.ForeignKey(to='pgameapp.Actor')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoinConversionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('coins', models.FloatField(verbose_name=b'Converted coins')),
                ('game_currency', models.FloatField(verbose_name=b'Received GC')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DepositHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('real_currency', models.FloatField(verbose_name=b'Real money')),
                ('game_currency', models.FloatField(verbose_name=b'Received GC')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_currency', models.CharField(default=b'Default game currency', max_length=30, verbose_name=b'game currency name')),
                ('coin_to_gc_rate', models.FloatField(default=1, verbose_name=b'coins to GC (game currency) rate')),
                ('coin_collect_time', models.PositiveIntegerField(default=10, verbose_name=b'interval (minutes) between coin collects')),
                ('min_coins_to_sell', models.FloatField(default=100, verbose_name=b'minimum coin balance to allow selling for GC')),
                ('investment_balance_percent_on_sale', models.PositiveSmallIntegerField(default=70, verbose_name=b'% GC to go to investment balance on coins sale')),
                ('first_deposit_bonus_percent', models.FloatField(default=0, verbose_name=b'% on 1st deposit bonus')),
                ('min_withdrawal_amount', models.FloatField(default=0, verbose_name=b'minimum withdrawal amount')),
                ('min_withdrawal_deposit_amount', models.FloatField(default=0, verbose_name=b'minimum deposit amount to allow withdrawals')),
                ('affiliate_deposit_percent', models.FloatField(default=0, verbose_name=b'affiliate deposit percent')),
                ('w_to_i_conversion_bonus_percent', models.PositiveSmallIntegerField(default=99, verbose_name=b'bonus (additional) percent on converting withdrawal to investment balance')),
            ],
            options={
                'verbose_name': 'game configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ManualGameStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('users_total', models.PositiveIntegerField(blank=True)),
                ('users_new_last_24', models.PositiveIntegerField(blank=True)),
                ('cash_total_paid', models.FloatField(blank=True)),
                ('cash_reserve', models.FloatField(blank=True)),
                ('project_duration_days', models.PositiveIntegerField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserActorOwnership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_actors', models.PositiveIntegerField(default=0, verbose_name=b'number of actors')),
                ('actor', models.ForeignKey(to='pgameapp.Actor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('crypto_address', models.CharField(max_length=50, blank=True)),
                ('pin', models.CharField(max_length=10, verbose_name=b'Personal PIN', blank=True)),
                ('balance_i', models.FloatField(default=0, verbose_name=b'Investment balance')),
                ('balance_w', models.FloatField(default=0, verbose_name=b'Withdrawal balance')),
                ('balance_coins', models.FloatField(default=0)),
                ('referral_id', models.CharField(unique=True, max_length=30)),
                ('last_coin_collection_time', models.DateTimeField(auto_now_add=True)),
                ('referrer', models.ForeignKey(related_name='referrals', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'UserProfile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WithdrawalHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('real_currency', models.FloatField(verbose_name=b'Real money received')),
                ('game_currency', models.FloatField(verbose_name=b'GC spent')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='useractorownership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='useractorownership',
            unique_together=set([('user', 'actor')]),
        ),
        migrations.AddField(
            model_name='deposithistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coinconversionhistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actorprocurementhistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actor',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='pgameapp.UserActorOwnership'),
            preserve_default=True,
        ),
    ]
