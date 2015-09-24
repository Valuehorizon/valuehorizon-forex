from django.contrib import admin
from forex.models import Currency, CurrencyPrice

class CurrencyAdmin(admin.ModelAdmin): 
    search_fields=["name", ]
    list_display = ('name', 'symbol', 'digits', 'num_code', 'ascii_symbol')
admin.site.register(Currency, CurrencyAdmin)

class CurrencyPriceAdmin(admin.ModelAdmin):
    list_filter=['currency']
    list_display = ('currency', 'date', 'ask_price', 'bid_price')
admin.site.register(CurrencyPrice, CurrencyPriceAdmin)


