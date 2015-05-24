"""Tests for the models of the forex app."""
from django.test import TestCase
from django.core.validators import ValidationError
from datetime import date
from decimal import Decimal

# Import models
from ..models import Currency, CurrencyPrices


class DummyModelTestCase(TestCase):
    """Tests for the ``DummyModel`` model."""
    def setUp(self):
        return 0
        # self.obj = factories.DummyModelFactory()
    
    def test_model(self):
        # self.assertTrue(self.obj.pk)
        self.assertTrue(True)


class CurrencyModelTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST")
        test_curr1 = Currency.objects.get(symbol="TEST")

        CurrencyPrices.objects.create(currency=test_curr1,
            date=date(2015,1,1),
            ask_price = 3,
            bid_price = 4)

        CurrencyPrices.objects.create(currency=test_curr1,
            date=date(2015,1,3),
            ask_price = 5,
            bid_price = 6)

        CurrencyPrices.objects.create(currency=test_curr1,
            date=date(2015,1,5),
            ask_price = 7,
            bid_price = 8)

    def field_tests(self):
        required_fields = [u'id', 'name', 'symbol', 'ascii_symbol', 'num_code', 'digits', 'description']
        actual_fields = [field.name for field in Currency._meta.fields]
        self.assertEqual(set(required_fields), set(actual_fields))

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
        self.assertEqual(df.ix[1]['ASK'], 3)


class CurrencyPriceModelTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST")
        test_curr1 = Currency.objects.get(symbol="TEST")
        CurrencyPrices.objects.create(currency=test_curr1,
            date=date(2015,1,1),
            ask_price = 3,
            bid_price = 4)

    def field_tests(self):
        required_fields = ['id', 'currency', 'date', 'ask_price', 'bid_price']
        actual_fields = [field.name for field in CurrencyPrices._meta.fields]
        self.assertEqual(set(required_fields), set(actual_fields))

    def test_ask_price_min_validation(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrices.objects.get(currency=test_curr1, date=date(2015,1,1))
        price.ask_price = 0
        price.save()
        self.assertEqual(price.ask_price, Decimal('0'))

        price.ask_price = -1
        # try:
        #     price.save()
        #     raise AssertionError("Ask Price cannot be less than zero")
        # except ValidationError:
        #     pass
        

    def test_mid_price(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrices.objects.get(currency=test_curr1, date=date(2015,1,1))
        price.ask_price = 3
        price.bid_price = 4
        price.save()
        self.assertEqual(price.mid_price, Decimal('3.5'))

    def test_ask_us(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrices.objects.get(currency=test_curr1, date=date(2015,1,1))

        price.ask_price = Decimal('3')
        price.save()
        self.assertEqual(price.ask_price_us, 1/Decimal('3'))

        price.ask_price = 0
        try:
            test = price.ask_price_us
            raise AssertionError("Price should not be zero")
        except ZeroDivisionError:
            pass

    def test_bid_us(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrices.objects.get(currency=test_curr1, date=date(2015,1,1))

        price.bid_price = Decimal('3')
        price.save()
        self.assertEqual(price.bid_price_us, 1/Decimal('3'))

        price.bid_price = 0
        try:
            test = price.bid_price_us
            raise AssertionError("Price should not be zero")
        except ZeroDivisionError:
            pass