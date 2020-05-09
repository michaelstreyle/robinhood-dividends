from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ViewSet
from django.db.models.functions import ExtractYear
from django.db.models import F, Sum, Count
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Tickers, Holdings, Dividends, CurrentValue
#from .serializers import TickerSerializer, HoldingsSerializer, DividendsSerializer 


@login_required
def home(request):
    # queryset = Holdings.objects.all()
    # serializer_class = HoldingsSerializer
    value = CurrentValue.objects.order_by('-date')
    holdings = Holdings.objects.order_by('-equity')
    labels = []
    data = []

    for day in CurrentValue.objects.order_by('date'):
        labels.append(day.date.strftime("%Y-%m-%d"))
        data.append(day.equity)
    
    #plot_data = [labels, data]

    return render(request, 'robinhood/home.html', {'holdings':holdings, 'value':value, 'labels': labels, 'data':data})


@login_required
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


@login_required
def Recommendations(request):
    return render(request, 'robinhood/sentiments.html', {})