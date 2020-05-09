from django.contrib import admin
from .models import  Tickers, Holdings, Dividends, CurrentValue


admin.site.register(Tickers)
admin.site.register(Holdings)
admin.site.register(Dividends)
admin.site.register(CurrentValue)

