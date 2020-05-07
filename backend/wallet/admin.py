from django.contrib import admin
from .models import Wallet, Instrument, Moviment
# Register your models here.


class AdminMoviment(admin.ModelAdmin):
    list_display = ["wallet", "instrument", "date", "quantity","total_investment", "total_costs"]
    search_fields = ["wallet__description","instrument__tckrSymb"]
    list_filter = ["wallet", ("instrument",admin.RelatedOnlyFieldListFilter)]
    exclude= ('type',)

class AdminWallet(admin.ModelAdmin):
    list_display = ['user', 'description']
    list_filter = ['user']


admin.site.register(Wallet,AdminWallet)

admin.site.register(Moviment,AdminMoviment)
