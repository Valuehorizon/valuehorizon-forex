from django.db import models
from django.db.models import Manager

# Import misc packages
import calendar as cal
import numpy as np
from datetime import date, datetime, timedelta
from decimal import Decimal
from pandas import DataFrame, date_range


class Currency(models.Model):
    """
    Represents a currency according to ISO 4217 standards.
    """

    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, unique=True)
    ascii_symbol = models.CharField(max_length=20, null=True, blank=True)
    num_code = models.IntegerField(null=True, blank=True)
    digits = models.IntegerField(null=True, blank=True)  # Digits after decimal (minor unit)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Currencies'
        verbose_name = 'Currency'
        ordering = ['symbol', ]

    def __unicode__(self):
        return u'%s %s %s' % (unicode(self.name), unicode(',  '), unicode(self.symbol))
    
    def generate_dataframe(self, start_date=None, end_date=None):
        """
        """
        first_series_point = CurrencyPrices.objects.filter(currency=self)[0]
        last_series_point = CurrencyPrices.objects.filter(currency=self).reverse()[0]
        if start_date == None:
            start_date = first_series_point.date
        else:
            start_date = max(first_series_point.date, start_date)
        # Get a one day lag so the change wont be null
        temp_start_date = start_date - timedelta(days=3)
        
        if end_date == None:
            end_date = last_series_point.date
        else:
            end_date = min(last_series_point.date, end_date)
            
        currency_date = CurrencyPrices.objects.filter(currency=self,
                                                      date__gte=temp_start_date,
                                                      date__lte=end_date).values_list('date', 'ask_price', 'bid_price')
        currency_data_array = np.core.records.fromrecords(currency_date, names=['DATE', "ASK", "BID"])
        df = DataFrame.from_records(currency_data_array, index='DATE')  
        df = df.astype(float)
        df['MID'] = (df['ASK'] + df['BID']) / 2.0
        df['CHANGE'] = df['MID'].pct_change()
        
        required_dates = date_range(start_date,end_date)
        df = df.reindex(required_dates)
        
        return df

    def save(self, *args, **kwargs):
        """
        Generates name and cached data
        """
        
        super(Currency, self).save(*args, **kwargs) # Call the "real" save() method.


class CurrencyPricesManager(Manager):
    """ Adds some added functionality """

    def generate_dataframe(self, symbols=None, date_index = None):
        """
        Generate a dataframe consisting of the currency prices (specified by symbols)
        from the start to end date
        """
        
        # Set defaults if necessary
        if symbols == None:
            symbols = Currency.objects.all().values_list('symbol')
        try:
            assert(date_index != None)
            assert(len(date_index > 0))
        except:
            start_date = date(2005,1,1)
            end_date = date.today()    
            date_index = date_range(start_date, end_date)
        
        currency_price_data = CurrencyPrices.objects.filter(currency__symbol__in=symbols, date__in=date_index.tolist()).values_list('date', 'currency__symbol', 'ask_price')
        try:
            # Generate numpy array from queryset data
            forex_data_array = np.core.records.fromrecords(currency_price_data, names=['date', 'symbol', 'ask_price'])
        except IndexError:
            # If there is no data, generate an empty array
            forex_data_array = np.core.records.fromrecords([(date(1900,1,1) ,"",0)], names=['date', 'symbol', 'ask_price'])
        df = DataFrame.from_records(forex_data_array, index='date')
        
        # Create pivot table
        df['date'] = df.index
        df = df.pivot(index='date', columns='symbol', values='ask_price')
        
        return df
        

class CurrencyPrices(models.Model):
    """
    Represents a currency price to US
    """

    currency = models.ForeignKey(Currency)
    date = models.DateField()
    
    # Price Data per $1 of US
    ask_price = models.DecimalField(max_digits=20, decimal_places=4,)
    bid_price = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    
    # Price Data US per 1 Unit of Currency
    ask_price_us = models.DecimalField(max_digits=20, decimal_places=4, editable=False)
    bid_price_us = models.DecimalField(max_digits=20, decimal_places=4, editable=False)
    
    # Add custom managers
    objects=CurrencyPricesManager()

    class Meta:
        verbose_name_plural = 'Currency Prices'
        verbose_name = 'Currency Price'
        ordering = ['date', ]
        unique_together=['date', 'currency']
        get_latest_by = "date"

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.currency),
                            unicode(self.date),)
    
    def mid_price(self):
        """
        Compute the mid point between bid and ask
        """
        if self.ask_price != None and self.bid_price != None:
            return (self.ask_price + self.bid_price) / Decimal('2.0')
        else:
            return None
    
    def save(self, *args, **kwargs):
        """
        Generates name
        """
        
        if self.ask_price != None and self.ask_price != 0:
            self.ask_price_us = 1 / Decimal(str(self.ask_price))
        if self.bid_price != None and self.bid_price != 0:
            self.bid_price_us = 1 / Decimal(str(self.bid_price))
        
        super(CurrencyPrices, self).save(*args, **kwargs) # Call the "real" save() method.


def convert_currency(from_symbol, to_symbol, value, date):
    """
    """
    if from_symbol == to_symbol:
        return value
    
    
    from_currency = Currency.objects.get(symbol=from_symbol)
    try:
        from_currency_price = CurrencyPrices.objects.get(currency=from_currency, date=date).mid_price()
    except CurrencyPrices.DoesNotExist:
        print "Cannot fetch prices for %s on %s" % (str(from_currency), str(date))
        return None
    
    to_currency = Currency.objects.get(symbol=to_symbol)
    try:
        to_currency_price = CurrencyPrices.objects.get(currency=to_currency, date=date).mid_price()
    except CurrencyPrices.DoesNotExist:
        print "Cannot fetch prices for %s on %s" % (str(to_currency), str(date))
        return None        
    
    if type(value) == float:
        output = (value / float(from_currency_price)) * float(to_currency_price)
    elif type(value) == Decimal:
        output = (value / Decimal(str(from_currency_price))) * Decimal(str(to_currency_price))
    else:
        output = None
    
    return output

