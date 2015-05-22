# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0002_auto_20150508_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyprices',
            name='ask_price_us',
            field=models.DecimalField(default=0, editable=False, max_digits=20, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currencyprices',
            name='bid_price_us',
            field=models.DecimalField(default=0, editable=False, max_digits=20, decimal_places=4),
            preserve_default=False,
        ),
    ]
