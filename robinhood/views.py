from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ViewSet
from django.db.models.functions import ExtractYear
from django.db.models import F, Sum, Count
from django.db.models.functions import Cast
from django.db.models import FloatField

from .models import Tickers, Holdings, Dividends
#from .serializers import TickerSerializer, HoldingsSerializer, DividendsSerializer 


# class TickerViewSet(ModelViewSet):
#     queryset = Tickers.objects.all()
#     serializer_class = TickerSerializer

def home(request):
    # queryset = Holdings.objects.all()
    # serializer_class = HoldingsSerializer
    holdings = Holdings.objects
    return render(request, 'robinhood/home.html', {'holdings':holdings})

# class DividendsByYearViewSet(ModelViewSet):
#     """ Here we want to summarize the Dividends by Year and by Ticker

#     """
#     serializer_class = DividendsSerializer

#     divs = Dividends.objects.all()

