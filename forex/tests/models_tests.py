"""Tests for the models of the forex app."""
from django.test import TestCase
from ..models import Currency, CurrencyPrices
from datetime import date
from decimal import Decimal

# from . import factories


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
        
    def test_if_saved(self):
        test = Currency.objects.get(symbol="TEST")
        test.save()


class CurrencyPriceModelTests(TestCase):
    def setUp(self):
        Currency.objects.create(name="Test Dollar", symbol="TEST")
        test_curr1 = Currency.objects.get(symbol="TEST")
        CurrencyPrices.objects.create(currency=test_curr1,
            date=date(2015,1,1),
            ask_price = 3,
            bid_price = 4)
        
    def test_mid_price(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrices.objects.get(currency=test_curr1, date=date(2015,1,1))
        price.ask_price = 3
        price.bid_price = 4
        price.save()
        self.assertEqual(price.mid_price(), Decimal('3.5'))

    def test_mid_price_negative(self):
        test_curr1 = Currency.objects.get(symbol="TEST")
        price = CurrencyPrices.objects.get(currency=test_curr1, date=date(2015,1,1))
        price.ask_price = -1
        price.bid_price = 4
        price.save()
        midprice = price.mid_price()
        self.assertEqual(midprice, Decimal('1.5'))

        price.ask_price = 2
        price.bid_price = -8
        price.save()
        self.assertEqual(price.mid_price(), Decimal('-3'))

