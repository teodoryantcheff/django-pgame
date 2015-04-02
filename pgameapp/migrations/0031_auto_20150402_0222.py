# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('pgameapp', '0030_auto_20150402_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLedger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=16, decimal_places=5)),
                ('type', models.CharField(max_length=10, choices=[(b'pmt', b'payment'), (b'b_rp', b'referral payment'), (b'b_fp', b'1st payment bonus')])),
                ('object_id1', models.PositiveIntegerField(null=True)),
                ('object_id2', models.PositiveIntegerField(null=True)),
                ('object_id3', models.PositiveIntegerField(null=True)),
                ('serialized_data', models.TextField(null=True)),
                ('object_type1', models.ForeignKey(related_name='log_items1', to='contenttypes.ContentType', null=True)),
                ('object_type2', models.ForeignKey(related_name='log_items2', to='contenttypes.ContentType', null=True)),
                ('object_type3', models.ForeignKey(related_name='log_items3', to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('timestamp',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='blockprocessinghistory',
            options={'verbose_name_plural': 'BlockProcessingHistory'},
        ),
        migrations.AlterField(
            model_name='actorprocurementhistory',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coinconversionhistory',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referralstats',
            name='amount',
            field=models.DecimalField(max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referralstats',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
