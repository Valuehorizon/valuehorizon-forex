# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0006_auto_20150524_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyprices',
            name='ask_price',
            field=models.DecimalField(max_digits=20, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='currencyprices',
            name='bid_price',
            field=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
