from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ViewSet
from django.db.models.functions import ExtractYear
from django.db.models import F, Sum, Count
from django.db.models.functions import Cast
from django.db.models import FloatField

from .models import Tickers, Holdings, Dividends, CurrentValue
#from .serializers import TickerSerializer, HoldingsSerializer, DividendsSerializer 



def home(request):
    # queryset = Holdings.objects.all()
    # serializer_class = HoldingsSerializer
    value = CurrentValue.objects
    holdings = Holdings.objects.order_by('-equity')
    return render(request, 'robinhood/home.html', {'holdings':holdings, 'value':value})



def dividends(request):
    byticker = Dividends.objects.values('ticker__ticker')\
    .annotate(yearlysum = Sum('amount'))\
    .order_by('-yearlysum')\
    .values('ticker__ticker', 'yearlysum')

    yearly = Dividends.objects.values('date')\
    .annotate(year = ExtractYear('date'))\
    .values('year')\
    .annotate(yearsum = Sum('amount'))\
    .values('year', 'yearsum')
    return render(request, 'robinhood/dividends.html', {'dividends': byticker, 'dividends_year': yearly})



def Recommendations(request):
    return render(request, 'robinhood/sentiments.html', {})