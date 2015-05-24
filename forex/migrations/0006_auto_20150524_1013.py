# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0005_auto_20150522_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currencyprices',
            name='ask_price_us',
        ),
        migrations.RemoveField(
            model_name='currencyprices',
            name='bid_price_us',
        ),
    ]
