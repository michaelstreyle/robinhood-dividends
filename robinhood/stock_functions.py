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

    def get_holdings_df(self):
        """Gets the currently owned stocked including
                Name
                Quantity
                Average Buy Price
                Current Price
                Current PE Ratio
                Current Equity

        """
        my_stocks = robin_stocks.build_holdings()
        df = pd.DataFrame.from_dict(my_stocks, orient='index')[['name', 'quantity', 'average_buy_price', 'price', 'pe_ratio', 'equity']]
        return df.head()



def get_dividends_df(username, password):
    """Gets total and YTD Dividend totals for each stock

    """
    div_dict = {}
    robin_stocks.login(username,password)
    my_dividends = robin_stocks.account.get_dividends()
    for n in my_dividends:
        name = robin_stocks.stocks.get_name_by_url(n['instrument'])
        if name in div_dict.keys():
            div_dict[name][n['payable_date']] = {'amount': n['amount'], 'rate':n['rate'], 'position':n['position']}
        else:
            div_dict[name] = {}
            div_dict[name][n['payable_date']] = {'amount': n['amount'], 'rate':n['rate'], 'position':n['position']}
    return pd.DataFrame.from_dict(div_dict, orient='index')

#robin_stocks.login(os.getenv('ROBIN_USERNAME'),os.getenv('ROBIN_PASSWORD'))
R = Robinhood()
print(R.get_holdings_df())


#robin_stocks.stocks.get_historicals - use this for graphs