# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currencyprices',
            name='is_monthly',
        ),
        migrations.RemoveField(
            model_name='currencyprices',
            name='name',
        ),
    ]
