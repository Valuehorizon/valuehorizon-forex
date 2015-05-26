# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0007_auto_20150526_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='currencyprices',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='currencyprices',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
