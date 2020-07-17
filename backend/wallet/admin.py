from django.contrib import admin
from .models import Wallet, Moviment
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



