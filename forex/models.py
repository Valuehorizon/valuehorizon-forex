from django.db import models
from django.db.models import Manager
from django.core.validators import MinValueValidator, ValidationError

# Import misc packages
import numpy as np
from datetime import date, timedelta
from decimal import Decimal
from pandas import DataFrame, date_range

PRICE_PRECISION = 4
DATEFRAME_START_DATE = date(2005, 1, 1)


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

    # Cached Data
    date_modified = models.DateTimeField(null=True, blank=True, editable=False, auto_now=True)
    date_created = models.DateTimeField(null=True, blank=True, editable=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Currencies'
        verbose_name = 'Currency'
        ordering = ['name', 'symbol']

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.name), unicode(self.symbol))

    def generate_dataframe(self, start_date=None, end_date=None):
        """
        """
        first_series_point = CurrencyPrice.objects.filter(currency=self)[0]
        last_series_point = CurrencyPrice.objects.filter(currency=self).reverse()[0]
        start_date = first_series_point.date if start_date is None else max(first_series_point.date, start_date)
        temp_start_date = start_date - timedelta(days=3)  # Add lag
        end_date = last_series_point.date if end_date is None else min(last_series_point.date, end_date)
        currency_date = CurrencyPrice.objects.filter(currency=self, date__gte=temp_start_date, date__lte=end_date).values_list('date', 'ask_price', 'bid_price')
        currency_data_array = np.core.records.fromrecords(currency_date, names=['DATE', "ASK", "BID"])
        df = DataFrame.from_records(currency_data_array, index='DATE').astype(float)
        df['MID'] = (df['ASK'] + df['BID']) / 2.0
        df['CHANGE'] = df['MID'].pct_change()

        required_dates = date_range(start_date, end_date)
        df = df.reindex(required_dates)
        df = df.fillna(method='ffill')

        return df

    def compute_return(self, start_date, end_date, rate="MID"):
        """
        Compute the return of the currency between two dates
        """
        if rate not in ["MID", "ASK", "BID"]:
            raise ValueError("Unknown rate type (%s)- must be 'MID', 'ASK' or 'BID'" % str(rate))

        if end_date <= start_date:
            raise ValueError("End date must be on or after start date")

        df = self.generate_dataframe(start_date=start_date, end_date=end_date)
        start_price = df.ix[start_date][rate]
        end_price = df.ix[end_date][rate]

        currency_return = (end_price / start_price) - 1.0

        return currency_return


class CurrencyPriceManager(Manager):
    """ Adds some added functionality """

    def generate_dataframe(self, symbols=None, date_index=None, price_type="mid"):
        """
        Generate a dataframe consisting of the currency prices (specified by symbols)
        from the start to end date
        """

        # Set defaults if necessary
        if symbols is None:
            symbols = list(Currency.objects.all().values_list('symbol', flat=True))
        try:
            start_date = date_index[0]
            end_date = date_index[-1]
        except:
            start_date = DATEFRAME_START_DATE
            end_date = date.today()
        date_index = date_range(start_date, end_date)

        currency_price_data = CurrencyPrice.objects.filter(currency__symbol__in=symbols,
                                                           date__gte=date_index[0],
                                                           date__lte=date_index[-1]).values_list('date', 'currency__symbol', 'ask_price', 'bid_price')
        try:
            forex_data_array = np.core.records.fromrecords(currency_price_data, names=['date', 'symbol', 'ask_price', 'bid_price'])
        except IndexError:
            forex_data_array = np.core.records.fromrecords([(date(1900, 1, 1), "", 0, 0)], names=['date', 'symbol', 'ask_price', 'bid_price'])
        df = DataFrame.from_records(forex_data_array, index='date')
        df['date'] = df.index

        if price_type == "mid":
            df['price'] = (df['ask_price'] + df['bid_price']) / 2
        elif price_type == "ask":
            df['price'] = df['ask_price']
        elif price_type == "bid":
            df['price'] = df['bid_price']
        else:
            raise ValueError("Incorrect price_type (%s) must be on of 'ask', 'bid' or 'mid'" % str(price_type))

        df = df.pivot(index='date', columns='symbol', values='price')
        df = df.reindex(date_index)
        df = df.fillna(method="ffill")
        unlisted_symbols = list(set(symbols) - set(df.columns))
        for unlisted_symbol in unlisted_symbols:
            df[unlisted_symbol] = np.nan
        df = df[symbols]

        return df


class CurrencyPrice(models.Model):
    """
    Represents a currency price to US
    """

    currency = models.ForeignKey(Currency)
    date = models.DateField()

    # Price Data per $1 of US
    ask_price = models.DecimalField(max_digits=20, decimal_places=PRICE_PRECISION,
                                    validators=[MinValueValidator(Decimal('0.00'))])
    bid_price = models.DecimalField(max_digits=20, decimal_places=PRICE_PRECISION,
                                    validators=[MinValueValidator(Decimal('0.00'))])

    # Cached Data
    date_modified = models.DateTimeField(null=True, blank=True, editable=False, auto_now=True)
    date_created = models.DateTimeField(null=True, blank=True, editable=False, auto_now_add=True)

    # Add custom managers
    objects = CurrencyPriceManager()

    class Meta:
        verbose_name_plural = 'Currency Prices'
        verbose_name = 'Currency Price'
        ordering = ['date', ]
        unique_together = ['date', 'currency']
        get_latest_by = "date"

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.currency),
                            unicode(self.date),)

    def save(self, *args, **kwargs):
        """
        Sanitation checks
        """
        if self.ask_price < 0:
            raise ValidationError("Ask price must be greater than zero")
        if self.bid_price < 0:
            raise ValidationError("Bid price must be greater than zero")
        if self.ask_price < self.bid_price:
            raise ValidationError("Ask price must be at least Bid price")

        super(CurrencyPrice, self).save(*args, **kwargs)  # Call the "real" save() method.

    @property
    def mid_price(self):
        """
        Compute the mid point between the bid and ask prices
        """
        return (self.ask_price + self.bid_price) / Decimal('2.0')

    @property
    def spread(self):
        """
        Compute the difference between bid and ask prices
        """
        return (self.ask_price - self.bid_price)

    @property
    def ask_price_us(self):
        """
        Calculate the ask_price in USD. This is the inverse
        of the ask price.
        """
        if self.ask_price != 0:
            return 1 / Decimal(str(self.ask_price))
        else:
            raise ZeroDivisionError('Ask price is zero')

    @property
    def bid_price_us(self):
        """
        Calculate the bid_price in USD. This is the inverse
        of the bid price.
        """
        if self.bid_price != 0:
            return 1 / Decimal(str(self.bid_price))
        else:
            raise ZeroDivisionError('Bid price is zero')


def conversion_factor(from_symbol, to_symbol, date):
    """
    Generates a multiplying factor used to convert two currencies
    """

    from_currency = Currency.objects.get(symbol=from_symbol)
    try:
        from_currency_price = CurrencyPrice.objects.get(currency=from_currency, date=date).mid_price
    except CurrencyPrice.DoesNotExist:
        print "Cannot fetch prices for %s on %s" % (str(from_currency), str(date))
        return None

    to_currency = Currency.objects.get(symbol=to_symbol)
    try:
        to_currency_price = CurrencyPrice.objects.get(currency=to_currency, date=date).mid_price
    except CurrencyPrice.DoesNotExist:
        print "Cannot fetch prices for %s on %s" % (str(to_currency), str(date))
        return None

    return to_currency_price / from_currency_price


def convert_currency(from_symbol, to_symbol, value, date):
    """
    Converts an amount of money from one currency to another on a specified date.
    """
    if from_symbol == to_symbol:
        return value

    factor = conversion_factor(from_symbol, to_symbol, date)

    if type(value) == float:
        output = value * float(factor)
    elif type(value) == Decimal:
        output = Decimal(format(value * factor, '.%sf' % str(PRICE_PRECISION)))
    elif type(value) in [np.float16, np.float32, np.float64, np.float128, np.float]:
        output = float(value) * float(factor)
    else:
        output = None

    return output
