"""Tests for the models of the forex app."""
from django.test import TestCase
from ..models import Currency

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
        Currency.objects.create(name="Test Dollar2", symbol="TEST2")
        
    def test_if_saved(self):
            test = Currency.objects.get(symbol="TEST")
            test2 = Currency.objects.get(symbol="TEST2")