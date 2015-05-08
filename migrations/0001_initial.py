# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(unique=True, max_length=10)),
                ('ascii_symbol', models.CharField(max_length=20, null=True, blank=True)),
                ('num_code', models.IntegerField(null=True, blank=True)),
                ('digits', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('latest_date', models.DateField(null=True, editable=False, blank=True)),
                ('latest_ask_price', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=4, blank=True)),
                ('latest_ask_price_us', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=4, blank=True)),
                ('latest_change', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('change_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('volatility_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ['symbol'],
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='CurrencyPrices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('ask_price', models.DecimalField(max_digits=20, decimal_places=4)),
                ('bid_price', models.DecimalField(null=True, max_digits=20, decimal_places=4, blank=True)),
                ('ask_price_us', models.DecimalField(null=True, max_digits=20, decimal_places=4, blank=True)),
                ('bid_price_us', models.DecimalField(null=True, max_digits=20, decimal_places=4, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_monthly', models.BooleanField(default=False)),
                ('currency', models.ForeignKey(to='forex.Currency')),
            ],
            options={
                'ordering': ['date'],
                'get_latest_by': 'date',
                'verbose_name': 'Currency Price',
                'verbose_name_plural': 'Currency Prices',
            },
        ),
        migrations.AlterUniqueTogether(
            name='currencyprices',
            unique_together=set([('date', 'currency')]),
        ),
    ]
