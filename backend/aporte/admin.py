from django.contrib import admin
from .models import *


class AdminInstrument(admin.ModelAdmin):
    list_display = ["tckrSymb", "sgmtNm", "mktNm", "sctyCtgyNm", "isin", "cFICd", "crpnNm", "corpGovnLvlNm"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["tckrSymb"]
    list_filter = ["sctyCtgyNm"]

    class Meta:
        verbose_name = "Admin Instrument"
        verbose_name_plural = "Admin Instruments"
        #ordering = ['tckrSymb']

class AdminMoviment(admin.ModelAdmin):
    list_display = ["wallet", "instrument", "date", "quantity","total_investment", "total_costs"]
    search_fields = ["wallet__description","instrument__tckrSymb"]
    list_filter = ["wallet", ("instrument",admin.RelatedOnlyFieldListFilter)]
    exclude= ('type',)
# Register your models here. #red :)
admin.site.register([Aporte,Grupo, Ativo, TipoAtivo])
admin.site.register(Instrument, AdminInstrument)
admin.site.register(Moviment,AdminMoviment)

