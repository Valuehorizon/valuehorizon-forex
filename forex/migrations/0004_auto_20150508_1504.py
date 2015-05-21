# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0003_auto_20150508_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='change_52_week',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='latest_ask_price',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='latest_ask_price_us',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='latest_change',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='latest_date',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='volatility_52_week',
        ),
    ]
