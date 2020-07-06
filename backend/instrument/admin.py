from django.contrib import admin
from wallet.models import Wallet, Moviment
from instrument.models import Instrument, PriceHistory, Company
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
import json
# Register your models here.
class AdminInstrument(admin.ModelAdmin):
    list_display = ["tckrSymb", "sgmtNm", "mktNm", "sctyCtgyNm", "isin", "cFICd", "crpnNm", "corpGovnLvlNm"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["tckrSymb"]
    list_filter = ["sctyCtgyNm"]

    class Meta:
        verbose_name = "Admin Instrument"
        verbose_name_plural = "Admin Instruments"
        #ordering = ['tckrSymb']

class AdminHistory(admin.ModelAdmin):
    list_display = ["instrument", "date", "open", "high", "low", "close", "adj_close", "volume", "lastUpdate", "updated_at"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["date","instrument__tckrSymb", "instrument__crpnNm"]
    list_filter = ["instrument"]
   

    class Meta:
        verbose_name = "Admin Instrument"
        verbose_name_plural = "Admin Instruments"
        ordering = ["instrument"]


admin.site.register(Instrument, AdminInstrument)
admin.site.register(PriceHistory, AdminHistory)
# admin.site.register(Company)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["instrument", "json_data"]
    search_fields = ["instrument__tckrSymb", "instrument__crpnNm"]
    list_filter = ["instrument"]

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    def json_data(self, obj):
        data = json.loads(obj.data)['data']
        display = json.loads(obj.data)['display']
        show = []
        for x,y in data.items():
            show.append("({} : {})".format(display[x],y))
        return show

        # for key, value in json.loads(obj.data)['data']:
        #     return "{0}: {1}".format(key, value)
        

    class Meta:
        verbose_name = "Admin Company"
        verbose_name_plural = "Admin Companies"
        ordering = ["instrument"]

