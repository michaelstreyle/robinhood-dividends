from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ViewSet
from django.db.models.functions import ExtractYear
from django.db.models import F, Sum, Count
from django.db.models.functions import Cast
from django.db.models import FloatField

from .models import Tickers, Holdings, Dividends, CurrentValue
#from .serializers import TickerSerializer, HoldingsSerializer, DividendsSerializer 


# class TickerViewSet(ModelViewSet):
#     queryset = Tickers.objects.all()
#     serializer_class = TickerSerializer

def home(request):
    # queryset = Holdings.objects.all()
    # serializer_class = HoldingsSerializer
    value = CurrentValue.objects
    holdings = Holdings.objects
    return render(request, 'robinhood/home.html', {'holdings':holdings, 'value':value})

# class DividendsByYearViewSet(ModelViewSet):
#     """ Here we want to summarize the Dividends by Year and by Ticker

#     """
#     serializer_class = DividendsSerializer

#     divs = Dividends.objects.all()


def dividends(request):
    # queryset = Holdings.objects.all()
    # serializer_class = HoldingsSerializer
    dividends = Dividends.objects  #instead, i should group by year and company
    return render(request, 'robinhood/dividends.html', {'dividends':dividends})


def sentiments(request):
    return ''