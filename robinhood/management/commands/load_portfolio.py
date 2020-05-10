#import dask.dataframe as dd
import os
import numpy as np
import pandas as pd 
import robin_stocks
from datetime import datetime
from django.core.management import BaseCommand
from django.db import transaction
from google.cloud import ndb

from ...models import Tickers, Holdings, Dividends, CurrentValue


class Settings(ndb.Model):
    """This is a class to retrieve credentials from DataStore

    Example Usage: Settings.get('ROBIN_USERNAME')


    """
    name = ndb.StringProperty()
    value = ndb.StringProperty()
    
    @staticmethod
    def get(name):
        client = ndb.Client()
        with client.context():
            NOT_SET_VALUE = "NOT SET"
            retval = Settings.query(Settings.name == name).get()
            if not retval:
                retval = Settings()
                retval.name = name
                retval.value = NOT_SET_VALUE
                retval.put()
            if retval.value == NOT_SET_VALUE:
                raise Exception(('Setting %s not found in the database. A placeholder ' +
                    'record has been created. Go to the Developers Console for your app ' +
                    'in App Engine, look up the Settings record with name=%s and enter ' +
                    'its value in that record\'s value field.') % (name, name))
            return retval.value



class Robinhood():
    """ A Class to contain Robinhood related methods
        allows only signing in once

    """
    def __init__(self):
        #self.username = os.getenv('ROBIN_USERNAME')
        #self.password = os.getenv('ROBIN_PASSWORD')
        self.username = Settings.get('ROBIN_USERNAME')
        self.password = Settings.get('ROBIN_PASSWORD')
        robin_stocks.login(self.username, self.password)
        self.holdings = robin_stocks.build_holdings()
        self.portfolio = robin_stocks.build_user_profile()
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

    def show_value(self):
        today = datetime.today().strftime('%Y-%m-%d') #'2020-03-11'
        return {'date':today, 'equity': self.portfolio['equity'], 'cash':self.portfolio['cash']}





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
        #CurrentValue.objects.all().delete()

        if options['mock']:
            #print('this would be fake data')
            #This is all made up data!
            holdings = {'AAPL': {'price': '300', 'quantity': '200', 'average_buy_price': '200', 'equity': '33211', 'pe_ratio': '11.5', 'name':'Apple'},\
             'USB': {'price': '34.94', 'quantity': '15.00', 'average_buy_price': '44.8213', 'equity': '524.10', 'pe_ratio': '9.04', 'name':'U.S. Bank'}, \
             'INTC': {'price': '57.50', 'quantity': '15.0', 'average_buy_price': '49.9533', 'equity': '862.50','pe_ratio': '11.13', 'name':'Intel'},
             'DAL': {'price': '34.94', 'quantity': '15.00', 'average_buy_price': '20', 'equity': '5240.10', 'pe_ratio': '9.04', 'name':'Delta Airlines'}, \
             'MET': {'price': '34.94', 'quantity': '120.00', 'average_buy_price': '20', 'equity': '52040.10', 'pe_ratio': '9.04', 'name':'Metlife'}, \
             'T': {'price': '29.94', 'quantity': '120.00', 'average_buy_price': '30', 'equity': '10000.10', 'pe_ratio': '14.04', 'name':'AT&T'}, \
             'IBM': {'price': '121.96', 'quantity': '100.00', 'average_buy_price': '122.2', 'equity': '1219.60', 'pe_ratio': '12.071000', 'name':'International Business Machines'}}
            holdings = pd.DataFrame.from_dict(holdings, orient='index')[['name', 'quantity', 'average_buy_price', 'price', 'pe_ratio', 'equity']]
            tickers_owned = ['AAPL', 'T', "USB", "JNJ", "INTC", 'IBM', 'DAL', 'LNT' , 'MET']
            dividends = {'2019-03-22': {'ticker': 'DAL', 'amount': '200', 'rate': '0.350', 'position': '5.0'}, 
                '2020-03-11': {'ticker': 'IBM', 'amount': '7.85', 'rate': '1.57', 'position': '5'}, 
                '2020-02-15': {'ticker': 'LNT', 'amount': '4.26', 'rate': '0.355', 'position': '12'},
                '2020-02-15': {'ticker': 'LNT', 'amount': '4.26', 'rate': '0.355', 'position': '12'},
                '2019-02-15': {'ticker': 'DAL', 'amount': '400', 'rate': '0.355', 'position': '12'},
                '2019-02-15': {'ticker': 'LNT', 'amount': '4.26', 'rate': '0.355', 'position': '12'},
                '2019-02-15': {'ticker': 'AAPL', 'amount': '4.26', 'rate': '0.355', 'position': '12'},
                '2019-02-15': {'ticker': 'IBM', 'amount': '4.26', 'rate': '0.355', 'position': '12'},
                }
            value = {'date':'2021-04-03', 'equity': '6666', 'cash': '6666'}
        else:
            #instantiate a Robinhood Class instance
            R = Robinhood()
            holdings = R.get_holdings_df()
            tickers_owned = holdings.index
            # get our dividend history
            dividends = R.get_dividends()
            value = R.show_value()

        # add stocks in our portfolio to the Tickers model
        Tickers.objects.bulk_create(
            [Tickers(ticker=record) for record in tickers_owned if record not in Tickers.objects.all()]
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

        CurrentValue.objects.create(date = value['date'], equity=value['equity'], cash=value['cash'])


