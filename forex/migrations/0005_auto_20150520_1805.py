# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0004_auto_20150508_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'ordering': ['name', 'symbol'], 'verbose_name': 'Currency', 'verbose_name_plural': 'Currencies'},
        ),
    ]
