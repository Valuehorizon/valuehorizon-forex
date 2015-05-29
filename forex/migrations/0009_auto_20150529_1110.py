# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0008_auto_20150526_1310'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurrencyPrices',
            new_name='CurrencyPrice',
        ),
    ]
