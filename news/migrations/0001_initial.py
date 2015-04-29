# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('summary', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'get_latest_by': 'timestamp',
                'verbose_name_plural': 'NewsEntries',
            },
            bases=(models.Model,),
        ),
    ]
