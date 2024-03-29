from django.contrib import admin
from wallet.models import Wallet, Moviment
from instrument.models import Instrument, PriceHistory, Company, Dividend, Split, Event, ProventoFII
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
import json
# Register your models here.
class AdminInstrument(admin.ModelAdmin):
    list_display = ["tckrSymb", "sgmtNm", "mktNm", "sctyCtgyNm", "isin", "cFICd", "crpnNm", "corpGovnLvlNm"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["tckrSymb", "sgmtNm", "mktNm", "sctyCtgyNm", "isin", "cFICd", "crpnNm", "corpGovnLvlNm"]
    list_filter = ["sctyCtgyNm"]

    class Meta:
        verbose_name = "Admin Instrument"
        verbose_name_plural = "Admin Instruments"
        #ordering = ['tckrSymb']

admin.site.register(Instrument, AdminInstrument)

class AdminHistory(admin.ModelAdmin):
    list_display = ["instrument", "date", "open", "high", "low", "close", "adj_close", "volume", "lastUpdate", "updated_at"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["date","instrument__tckrSymb", "instrument__crpnNm"]
    list_filter = ["instrument"]
   

    class Meta:
        verbose_name = "Admin Instrument"
        verbose_name_plural = "Admin Instruments"
        ordering = ["instrument"]

admin.site.register(PriceHistory, AdminHistory)


### yEvents Source
class AdminEvent(admin.ModelAdmin):
    list_display = ['instrument', 'dividends', 'stock_splits', 'event_date']
    search_fields = ["event_date","instrument__tckrSymb", "instrument__crpnNm"]
    list_filter = ['instrument']

admin.site.register(Event, AdminEvent)


class AdminDividend(admin.ModelAdmin):
    list_display = ["instrument", "ex_date", "event_date", "category", "value", "adjusted_value"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["event_date","instrument__tckrSymb", "instrument__crpnNm", "category"]
    list_filter = ["category"]
   

    class Meta:
        verbose_name = "Admin Dividend"
        verbose_name_plural = "Admin Dividends"
        ordering = ["-event_date"]

admin.site.register(Dividend, AdminDividend)


class AdminSplit(admin.ModelAdmin):
    list_display = ["instrument", "ex_date", "event_date", "category", "factor"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["event_date","instrument__tckrSymb", "instrument__crpnNm", "category"]
    list_filter = ["instrument", "category"]
   

    class Meta:
        verbose_name = "Admin Split"
        verbose_name_plural = "Admin Splits"
        ordering = ["-event_date"]

admin.site.register(Split, AdminSplit)
class AdminProventoFII(admin.ModelAdmin):
    list_display = ["instrument", "ex_date", "payment_date", "category", "value"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["ex_date","payment_date","instrument__tckrSymb", "instrument__crpnNm", "category"]
    list_filter = ["category"]
   

    class Meta:
        verbose_name = "Admin Provento FII"
        verbose_name_plural = "Admin Proventos FIIs"
        ordering = ["ex_date"]

admin.site.register(ProventoFII, AdminProventoFII)

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

