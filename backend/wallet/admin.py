from django.contrib import admin
from .models import Wallet, Moviment
from instrument.models import Event, Instrument
# Register your models here.


class AdminMoviment(admin.ModelAdmin):
    list_display = ["wallet", "instrument", "date", "quantity","total_investment", "total_costs"]
    search_fields = ["wallet__description","instrument__tckrSymb"]
    list_filter = ["wallet", ("instrument",admin.RelatedOnlyFieldListFilter)]
    exclude= ('type',)

class AdminWallet(admin.ModelAdmin):
    list_display = ['user', 'description', "get_moviments"] # Movements estão aqui para teste... o correto seria Position
    list_filter = ['user']



class AdminEvent(admin.ModelAdmin):
    list_display = ['instrument', 'dividends', 'stock_splits', 'event_date']
    list_filter = ['instrument']


admin.site.register(Wallet, AdminWallet)
admin.site.register(Moviment, AdminMoviment)
admin.site.register(Event, AdminEvent)
