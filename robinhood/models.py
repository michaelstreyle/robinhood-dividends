from django.db import models


class Tickers(models.Model):
    """ This is a model to hold stock tickers from holdings and dividend history

    """
    ticker = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return '%s' % (self.ticker)

class Holdings(models.Model):
    """ This is a model to hold the current holdings

    """
    ticker = models.ForeignKey(Tickers, on_delete=models.CASCADE)
    quantity = models.FloatField()
    avg_cost = models.FloatField()
    pe_ratio = models.FloatField()
    current_price = models.FloatField()
    equity = models.FloatField()

    def __str__(self):
        return '%s__%s' % (self.ticker, self.equity)


class Dividends(models.Model):
    """ This is a model to hold the dividend history

    """
    ticker = models.ForeignKey(Tickers, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return 'Dividend Payment on %s from %s' % (self.date, self.ticker)

class CurrentValue(models.Model):
    date = models.DateField() #this format '2020-03-11'
    equity = models.FloatField()
    cash = models.FloatField()

    