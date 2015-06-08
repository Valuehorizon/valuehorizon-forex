# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0009_auto_20150529_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyprice',
            name='bid_price',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
            preserve_default=False,
        ),
    ]
