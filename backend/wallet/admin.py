from django.contrib import admin
from .models import Wallet, Moviment, Position
from instrument.models import Instrument
# Register your models here.


class AdminMoviment(admin.ModelAdmin):
    list_display = ["wallet", "instrument", "date", "quantity","total_investment", "total_costs"]
    search_fields = ["wallet__description","instrument__tckrSymb"]
    list_filter = ["wallet", ("instrument",admin.RelatedOnlyFieldListFilter)]
    exclude= ('type',)

admin.site.register(Moviment, AdminMoviment)

class AdminWallet(admin.ModelAdmin):
    list_display = ['user', 'description']
    list_filter = ['user']

admin.site.register(Wallet, AdminWallet)

class AdminPosition(admin.ModelAdmin):
    list_display = ["wallet", "instrument", "category","date", "quantity","total_quantity", "transaction_value", "net_value", "total_value", "total_selic"]
    search_fields = ["wallet__description","instrument__tckrSymb", "category"]
    list_filter = ["category", "wallet", ("instrument",admin.RelatedOnlyFieldListFilter)]
admin.site.register(Position, AdminPosition)

