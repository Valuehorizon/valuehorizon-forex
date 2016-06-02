"""Tests for the models of the forex app."""

# Import Django libraries
from django.test import TestCase
from django.core.validators import ValidationError

# Import Valuehorizon libraries
from ..models import Currency, CurrencyPrice, convert_currency
from ..models import DATEFRAME_START_DATE

# Import other libraries
from datetime import date
from decimal import Decimal
import pandas as pd


class CurrencyModelTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST")
        test_curr1 = Currency.objects.get(symbol="TEST")

        CurrencyPrice.objects.create(currency=test_curr1,
            date=date(2015, 1, 1),
            ask_price=4,
            bid_price=3)

        CurrencyPrice.objects.create(currency=test_curr1,
            date=date(2015, 1, 3),
            ask_price=6,
            bid_price=5)

        CurrencyPrice.objects.create(currency=test_curr1,
            date=date(2015, 1, 5),
            ask_price=8,
            bid_price=7)

    def field_tests(self):
        required_fields = [u'id', 'name', 'symbol', 'ascii_symbol', 'num_code', 'digits', 'description', 'date_created', 'date_modified']
        actual_fields = [field.name for field in Currency._meta.fields]
        self.assertEqual(set(required_fields), set(actual_fields))

    def test_unicode(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        test_curr1.save()
        self.assertEqual(test_curr1.__unicode__(), "Test Dollar, TEST")

    def test_dataframe_generation_base(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        df = test_curr1.generate_dataframe()
        self.assertEqual(len(df.columns), 4)
        self.assertTrue('ASK' in df.columns)
        self.assertTrue('BID' in df.columns)
        self.assertTrue('CHANGE' in df.columns)
        self.assertTrue('MID' in df.columns)

    def test_dataframe_generation_mid(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        df = test_curr1.generate_dataframe()
        self.assertEqual(df.ix[0]['MID'], (df.ix[0]['ASK'] + df.ix[0]['BID']) / 2.0)

    def test_dataframe_generation_fill(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        df = test_curr1.generate_dataframe()
        self.assertEqual(df.ix[1]['ASK'], 4)


class CurrencyPriceModelTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST")
        test_curr1 = Currency.objects.get(symbol="TEST")
        CurrencyPrice.objects.create(currency=test_curr1,
            date=date(2015, 1, 1),
            ask_price=4,
            bid_price=3)

    def field_tests(self):
        required_fields = ['id', 'currency', 'date', 'ask_price', 'bid_price', 'date_created', 'date_modified']
        actual_fields = [field.name for field in CurrencyPrice._meta.fields]
        self.assertEqual(set(required_fields), set(actual_fields))

    def test_unicode(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        test_curr1.save()
        test_price1 = CurrencyPrice.objects.get(currency=test_curr1,
                                                date=date(2015, 1, 1))
        test_price1.save()
        self.assertEqual(test_price1.__unicode__(), "Test Dollar, TEST, 2015-01-01")

    def test_ask_price_min_validation(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015, 1, 1))
        price.ask_price = 0
        price.bid_price = 0
        price.save()
        self.assertEqual(price.ask_price, Decimal('0'))

        price.ask_price = -1
        try:
            price.save()
            raise AssertionError("Ask Price cannot be less than zero")
        except ValidationError:
            pass

    def test_bid_price_min_validation(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015,
                                                                         1, 1))
        price.bid_price = 0
        price.save()
        self.assertEqual(price.bid_price, Decimal('0'))

        price.bid_price = -1
        try:
            price.save()
            raise AssertionError("Bid Price cannot be less than zero")
        except ValidationError:
            pass

    def test_bid_ask_validity(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015, 1, 1))

        price.bid_price = 50
        price.ask_price = 40
        try:
            price.save()
            raise AssertionError("Ask price must be greater than or equal to Bid price")
        except ValidationError:
            pass

        price.bid_price = 40
        price.ask_price = 50
        self.assertEqual(price.save(), None)

        price.bid_price = 50
        price.ask_price = 50
        self.assertEqual(price.save(), None)

    def test_mid_price(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015, 1, 1))
        price.ask_price = 5
        price.bid_price = 4
        price.save()
        self.assertEqual(price.mid_price, Decimal('4.5'))

    def test_spread(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015, 1, 1))
        price.ask_price = 4
        price.bid_price = 3
        price.save()
        self.assertEqual(price.spread, 4 - 3)

    def test_ask_us(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015, 1, 1))

        price.ask_price = Decimal('3')
        price.save()
        self.assertEqual(price.ask_price_us, 1 / Decimal('3'))

        price.ask_price = 0
        try:
            price.ask_price_us
            raise AssertionError("Price should not be zero")
        except ZeroDivisionError:
            pass

    def test_bid_us(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrice.objects.get(currency=test_curr1, date=date(2015, 1, 1))
        price.bid_price = Decimal('3')
        price.save()
        self.assertEqual(price.bid_price_us, 1 / Decimal('3'))

        price.bid_price = 0
        try:
            price.bid_price_us
            raise AssertionError("Price should not be zero")
        except ZeroDivisionError:
            pass


class CurrencyPriceDataFrame(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST1")
        Currency.objects.create(name="Test Dollar2", symbol="TEST2")
        Currency.objects.create(name="Test Dollar3", symbol="TEST3")
        test_curr1 = Currency.objects.get(symbol="TEST1")
        test_curr2 = Currency.objects.get(symbol="TEST2")

        CurrencyPrice.objects.create(currency=test_curr1, date=date(2015, 1, 1), ask_price=4, bid_price=3)
        CurrencyPrice.objects.create(currency=test_curr1, date=date(2015, 1, 15), ask_price=8, bid_price=6)
        CurrencyPrice.objects.create(currency=test_curr2, date=date(2015, 2, 1), ask_price=10, bid_price=9)
        CurrencyPrice.objects.create(currency=test_curr2, date=date(2015, 2, 15), ask_price=11, bid_price=7)

    def test_correct_rate_input(self):
        self.assertRaisesMessage(ValueError,
                                 "Incorrect price_type (*BAD*) must be on of 'ask', 'bid' or 'mid'",
                                 CurrencyPrice.objects.generate_dataframe,
                                 symbols=None,
                                 date_index=None,
                                 price_type="*BAD*")

    def test_no_symbols_no_dates(self):
        df = CurrencyPrice.objects.generate_dataframe(symbols=None, date_index=None)
        self.assertEqual(set(df.columns), set(["TEST1", "TEST2", "TEST3"]))
        self.assertEqual(set(df.index), set(pd.date_range(DATEFRAME_START_DATE, date.today())))

    def test_with_symbols_and_dates(self):
        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST1", "TEST2"], date_index=pd.date_range(date(2015, 1, 12), date(2015, 1, 26)))
        self.assertEqual(set(df.columns), set(["TEST1", "TEST2"]))
        self.assertEqual(set(df.index), set(pd.date_range(date(2015, 1, 12), date(2015, 1, 26))))

    def test_nodata(self):
        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST3"], date_index=None)
        self.assertEqual(set(df.index), set(pd.date_range(DATEFRAME_START_DATE, date.today())))
        self.assertEqual(set(df.columns), set(["TEST3"]))
        for datapoint in df["TEST3"]:
            self.assertEqual(pd.np.isnan(datapoint), True)

    def test_fill(self):
        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST1", "TEST2"], date_index=None)
        self.assertEqual(set(df.columns), set(["TEST1", "TEST2"]))
        self.assertEqual(set(df.index), set(pd.date_range(DATEFRAME_START_DATE, date.today())))
        self.assertEqual(df.loc[date(2015, 1, 10)]['TEST1'], Decimal('3.5'))

    def test_price_types(self):
        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST1", "TEST2"], date_index=None)
        self.assertEqual(df.loc[date(2015, 1, 10)]['TEST1'], Decimal('3.5'))

        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST1", "TEST2"], date_index=None, price_type="mid")
        self.assertEqual(df.loc[date(2015, 1, 10)]['TEST1'], Decimal('3.5'))

        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST1", "TEST2"], date_index=None, price_type='ask')
        self.assertEqual(df.loc[date(2015, 1, 10)]['TEST1'], Decimal('4'))

        df = CurrencyPrice.objects.generate_dataframe(symbols=["TEST1", "TEST2"], date_index=None, price_type="bid")
        self.assertEqual(df.loc[date(2015, 1, 10)]['TEST1'], Decimal('3'))


class ComputeReturnTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST1")
        test_curr1 = Currency.objects.get(symbol="TEST1")

        CurrencyPrice.objects.create(currency=test_curr1, date=date(2015, 1, 1), ask_price=4, bid_price=2)
        CurrencyPrice.objects.create(currency=test_curr1, date=date(2015, 1, 15), ask_price=8, bid_price=6)

    def test_bad_input_rate(self):
        test_curr1 = Currency.objects.get(symbol="TEST1")
        self.assertRaisesMessage(ValueError,
                                 "Unknown rate type (*BAD*)- must be 'MID', 'ASK' or 'BID'",
                                 test_curr1.compute_return,
                                 date(2015, 1, 2),
                                 date(2015, 1, 5),
                                 rate="*BAD*")

    def test_bad_input_dates(self):
        test_curr1 = Currency.objects.get(symbol="TEST1")
        self.assertRaisesMessage(ValueError,
                                 "End date must be on or after start date",
                                 test_curr1.compute_return,
                                 date(2015, 1, 10),
                                 date(2015, 1, 5),
                                 rate="MID")

    def test_computation(self):
        test_curr1 = Currency.objects.get(symbol="TEST1")
        self.assertEqual(test_curr1.compute_return(start_date=date(2015, 1, 1), end_date=date(2015, 1, 15), rate="MID"), (7. / 3) - 1)
        self.assertEqual(test_curr1.compute_return(start_date=date(2015, 1, 1), end_date=date(2015, 1, 15)), (7. / 3) - 1)
        self.assertEqual(test_curr1.compute_return(start_date=date(2015, 1, 1), end_date=date(2015, 1, 15), rate="ASK"), 1)
        self.assertEqual(test_curr1.compute_return(start_date=date(2015, 1, 1), end_date=date(2015, 1, 15), rate="BID"), 2)


class ConvertCurrencyTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST")
        test_curr1 = Currency.objects.get(symbol="TEST")
        CurrencyPrice.objects.create(currency=test_curr1,
            date=date(2015, 1, 1),
            ask_price=4,
            bid_price=3)

        Currency.objects.create(name="Test Dollar2", symbol="TEST2")
        test_curr2 = Currency.objects.get(symbol="TEST2")
        CurrencyPrice.objects.create(currency=test_curr2,
            date=date(2015, 1, 1),
            ask_price=8,
            bid_price=6)

        Currency.objects.create(name="Test Dollar3", symbol="TEST3")
        test_curr2 = Currency.objects.get(symbol="TEST3")
        CurrencyPrice.objects.create(currency=test_curr2,
            date=date(2016, 1, 1),
            ask_price=10,
            bid_price=9)

    def test_convert_equal_currency(self):
        self.assertEqual(convert_currency("TEST", "TEST", 45, date(2015, 1, 1)), 45)
        self.assertEqual(convert_currency("TEST", "TEST", -45, date(2015, 1, 1)), -45)
        self.assertEqual(convert_currency("TEST", "TEST", 45, date(2015, 1, 30)), 45)
        self.assertEqual(convert_currency("TEST", "TEST", -45, date(2015, 1, 30)), -45)

    def test_convert_currency_no_data(self):
        self.assertEqual(convert_currency("TEST", "TEST2", -45, date(2015, 1, 15)), None)
        self.assertEqual(convert_currency("TEST", "TEST3", -45, date(2015, 1, 1)), None)

    def test_convert_currency_float(self):
        self.assertEqual(convert_currency("TEST", "TEST2", float(4.5), date(2015, 1, 1)), float(9))
        self.assertEqual(convert_currency("TEST", "TEST2", pd.np.float(4.5), date(2015, 1, 1)), pd.np.float(9))
        self.assertEqual(convert_currency("TEST", "TEST2", pd.np.float16(4.5), date(2015, 1, 1)), pd.np.float16(9))
        self.assertEqual(convert_currency("TEST", "TEST2", pd.np.float32(4.5), date(2015, 1, 1)), pd.np.float32(9))
        self.assertEqual(convert_currency("TEST", "TEST2", pd.np.float64(4.5), date(2015, 1, 1)), pd.np.float64(9))
        self.assertEqual(convert_currency("TEST", "TEST2", pd.np.float128(4.5), date(2015, 1, 1)), pd.np.float128(9))
        self.assertEqual(convert_currency("TEST", "TEST2", 4.5, date(2015, 1, 1)), 9.0)
        self.assertEqual(convert_currency("TEST", "TEST2", Decimal('4.5'), date(2015, 1, 1)), Decimal('9.0000'))
        self.assertEqual(convert_currency("TEST", "TEST2", '-45', date(2015, 1, 1)), None)
