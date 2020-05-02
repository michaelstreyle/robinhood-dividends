import dask.dataframe as dd
import os
import numpy as np
import pandas as pd 
import robin_stocks

from django.core.management import BaseCommand
from django.db import transaction
from ...models import Tickers, Holdings, Dividends




class Robinhood():
    """ A Class to contain Robinhood related methods
        allows only signing in once

    """
    def __init__(self):
        self.username = os.getenv('ROBIN_USERNAME')
        self.password = os.getenv('ROBIN_PASSWORD')
        robin_stocks.login(self.username, self.password)
        self.holdings = robin_stocks.build_holdings()
        self.ticker_map = {self.holdings[v]['name']:v for v in self.holdings.keys()}

    def get_holdings_df(self):
        """Gets the currently owned stocked including
                Name
                Quantity
                Average Buy Price
                Current Price
                Current PE Ratio
                Current Equity

        """
        df = pd.DataFrame.from_dict(self.holdings, orient='index')[['name', 'quantity', 'average_buy_price', 'price', 'pe_ratio', 'equity']]
        return df

    def get_dividends(self):
        """Gets total and YTD Dividend totals for each stock

        """
        div_dict = {}
        my_dividends = robin_stocks.account.get_dividends()
        for n in my_dividends:
            ticker = robin_stocks.stocks.get_symbol_by_url(n['instrument'])
            if ticker in div_dict.keys():
                div_dict[n['payable_date']] = {'ticker':ticker, 'amount': n['amount'], 'rate':n['rate'], 'position':n['position']}
            else:
                div_dict[n['payable_date']] = {}
                div_dict[n['payable_date']] = {'ticker':ticker, 'amount': n['amount'], 'rate':n['rate'], 'position':n['position']}
        return div_dict

    def dividend_summary(self):
        """ Returns a yearly total of dividend payments for each holding

        """
        d = self.get_dividends()
        df = pd.DataFrame.from_dict(d, orient='index')[['ticker', 'amount']].astype({'amount':'float'})
        df.index = pd.to_datetime(df.index)
        div_summary = df.groupby([df.index.year, df.ticker]).sum()
        return div_summary



class Command(BaseCommand):
    help = "Load portfolio"

    def add_arguments(self, parser):
        parser.add_argument("-m", "--mock", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        # Flush the models
        Tickers.objects.all().delete()
        Holdings.objects.all().delete()
        Dividends.objects.all().delete()

        if options['mock']:
            print('this would be fake data')
            holdings = pd.DataFrame()
            tickers_owned = []
            dividends = {}
        else:
            #instantiate a Robinhood Class instance
            R = Robinhood()
            holdings = R.get_holdings_df()
            tickers_owned = holdings.index
            # get our dividend history
            dividends = R.get_dividends()

        # add stocks in our portfolio to the Tickers model
        Tickers.objects.bulk_create(
            [Tickers(ticker=record) for record in tickers_owned]
        )        
        holdings['ticker'] = holdings.index

        # add stocks to our Holdings Model
        records = holdings.to_dict("records")
        instances = [
            Holdings(
                ticker=Tickers.objects.get(ticker=record["ticker"]),
                quantity=record["quantity"],
                avg_cost=record["average_buy_price"],
                pe_ratio=record["pe_ratio"],
                current_price=record["price"],
                equity=record["equity"],
            )
            for record in records
        ]
        Holdings.objects.bulk_create(instances)

        # add dividend stocks to ticker model if not already there
        # this is because I may have dividend history for a stock no longer in my portfolio
        for i in dividends:
            Tickers.objects.get_or_create(
                ticker = dividends[i]['ticker']
            )

        # add the dividend payments to my Dividends Model
        divs = [Dividends(
            ticker = Tickers.objects.get(ticker=dividends[record]["ticker"]),
            date = record,
            amount = dividends[record]["amount"],
                )
        for record in dividends
        ]
        Dividends.objects.bulk_create(divs)
