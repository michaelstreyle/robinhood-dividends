import pandas as pd 
import numpy as np 
import os
import robin_stocks




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
        return df.head()

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
        #print(div_summary.sum())


R = Robinhood()
d = R.dividend_summary()




#robin_stocks.stocks.get_historicals - use this for graphs