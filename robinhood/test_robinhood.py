from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Tickers, Holdings, Dividends, CurrentValue
from .views import home, dividends, Recommendations
from django.urls import reverse, resolve
from .urls import urlpatterns



class ModelTestCaseTicker(TestCase):
    """Test adding and counting records  
    """
    def setUp(self):
        Tickers.objects.create(ticker="IBM")
        Tickers.objects.create(ticker="AAPL")

    def test_ticker(self):
        """
        Test tickers are being added to the model correctly
        """
        first_ticker = Tickers.objects.get(ticker="IBM")
        self.assertEqual(first_ticker.__str__(), "IBM") 
        self.assertEqual(2, Tickers.objects.count())

class ModelTestCaseHoldings(TestCase):
    """Test adding and counting records in Holdings Model

    """
    def setUp(self):
        Tickers.objects.create(ticker="IBM")
        d = Tickers.objects.get(ticker="IBM")
        Holdings.objects.create(
            ticker = d,
            quantity = 10,
            avg_cost = 100,
            pe_ratio = 12,
            current_price = 122,
            equity = 1020
        )


    def test_Holdings(self):
        """
        Test records are being added and counted correctly in the Holdings Model
        """
        d = Tickers.objects.get(ticker="IBM")
        hold = Holdings.objects.get(ticker=d)
        self.assertEqual(hold.quantity, 10)  
        self.assertEqual(hold.avg_cost, 100)
        self.assertEqual(hold.pe_ratio, 12)
        self.assertEqual(hold.current_price, 122)
        self.assertEqual(hold.equity, 1020)


class ModelTestCaseDividends(TestCase):
    """Test adding and counting records in Dividends Model

    """
    def setUp(self):
        Tickers.objects.create(ticker="IBM")
        d = Tickers.objects.get(ticker="IBM")
        Dividends.objects.create(
            ticker = d,
            date = "2010-04-24",
            amount = 15.3,
        )


    def test_Dividends(self):
        """
        Test records are being added and counted correctly in the Dividends Model
        """
        d = Tickers.objects.get(ticker="IBM")
        div = Dividends.objects.get(ticker=d)
        self.assertEqual(div.date.strftime("%Y-%m-%d"), "2010-04-24")
        self.assertEqual(div.amount, 15.3)



        