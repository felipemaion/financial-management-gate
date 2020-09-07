from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
import yfinance as yf
from core.models import BaseTimeModel
from account.models import User
from django.contrib.postgres.fields import JSONField
# Create your models here.


class Instrument(BaseTimeModel):
    tckrSymb = models.CharField('tckrSymb', max_length=20, unique=True)
    sgmtNm = models.CharField('sgmtNm', max_length=255, blank=True, null=True)
    mktNm = models.CharField('mktNm', max_length=255, blank=True, null=True)
    sctyCtgyNm = models.CharField(
        "SctyCtgyNm", max_length=255, blank=True, null=True)
    isin = models.CharField('isin', max_length=50, blank=True, null=True)
    cFICd = models.CharField('cFICd', max_length=50, blank=True, null=True)
    crpnNm = models.CharField('crpnNm', max_length=50, blank=True, null=True)
    corpGovnLvlNm = models.CharField(
        'corpGovnLvlNm', max_length=255, blank=True, null=True)
    lastUpdate = models.DateTimeField('last update', blank=True, null=True)
    external_id = models.IntegerField('external id', blank=True, null=True)
    codigoCvm = models.IntegerField('codigoCvm', blank=True, null=True)

    def history(self):
        return yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            # This .SA is for South America (since the instruments are (for now) from SA). Future bug reported.
            tickers=self.tckrSymb + ".SA",

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period="max",

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval="1d",

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by='ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust=True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost=True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads=True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy=None
        )

    def populate_events(self):
        # Não me parece ser correto isso ser aqui. Está certo? TODO
        # This .SA is for South America (since the instruments are (for now) from SA).
        #  Future bug reported.
        events = None
        try:
            stock = yf.Ticker(self.tckrSymb + ".SA")
            events = stock.actions

        except:
            pass
        return events
        # In [58]: stock = yf.Ticker("MGLU3.SA")
        # In [59]: h = stock.history(period="max")
        # In [60]: h[h["Stock Splits"]!=0]
        # Out[60]:
        #             Open   High    Low  Close    Volume  Dividends  Stock Splits
        # Date
        # 2015-10-01   0.13   0.14   0.13   0.13  23648000        0.0         0.125
        # 2017-09-05   9.02   9.77   8.88   9.27  23837600        0.0         8.000
        # 2019-08-06  35.34  36.80  35.28  36.35  17456100        0.0         8.000

    def get_price(self, date=datetime.now()):
        try:
            # data = yf.download(self.tckrSymb + '.SA', date)
            data = PriceHistory.objects.filter(instrument=self).latest('date').adj_close
            return data
        except:
            return 0
    get_price.short_description = 'Price'
    get_price.admin_order_field = 'instrument__price'

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['tckrSymb']

    def __str__(self):
        return "{}: {}".format(self.tckrSymb, self.crpnNm)


class Event(BaseTimeModel):
    instrument = models.ForeignKey(Instrument, related_name="events",
                                   on_delete=models.CASCADE)
    event_date = models.DateField(
        'event date')  # precisa mesmo armazenar hora?
    dividends = models.DecimalField(
        'dividends', decimal_places=6, max_digits=20)
    stock_splits = models.DecimalField(
        'stock splits', decimal_places=6, max_digits=20
    )

    def __str__(self):
        return 'Ticker:{} Date:{} Dividends: {} Stock Splits: {}' .format(
            self.instrument.tckrSymb,
            str(self.event_date),
            str(self.dividends),
            str(self.stock_splits)
            )

    class Meta:
        unique_together = ('instrument', 'event_date',)
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-event_date']


class EventoAcao(BaseTimeModel):
    """
            instrument: "Instrument", 
            source_user: "SourceUser",
            ex_date: "DataEx",
            event_date: "DataPagamento"/"DataEvento",
            accounting_date": DataContabil",
            category: "Tipo",
            document_link: "LinkComunicado"
    """
    instrument = models.ForeignKey(Instrument, related_name="events2",
                on_delete=models.DO_NOTHING)

    source_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    ex_date = models.DateField(
        'ex-date')  # precisa mesmo armazenar hora?
    event_date = models.DateField(
        'payment date', blank=True, null=True)
    accounting_date = models.DateField(
        'accounting date', blank=True, null=True)
    
    category = models.CharField('category', max_length=20)

    document_link = models.URLField(max_length=1000, blank=True, null=True)
    class Meta:
        unique_together = ('instrument', 'ex_date','category', 'event_date')
        abstract = True
        verbose_name = 'event2'
        verbose_name_plural = 'events2'
        ordering = ['-ex_date']

class Dividend(EventoAcao):
    """
            instrument: "Instrument": << AÇÃO >> 
            source_user: "SourceUser": << USER WHO UPLOADED INFO >>,
            ex_date: "DataEx": "<< data apartir de quando não vale o evento, inclusa. >>",
            event_date: "DataPagamento": "<<  data do pagamento >>",
            accounting_date: "DataContabil": "<< data contábil >>",
            category: "Tipo": "DIV" / "JCP" ,
            document_link: "LinkComunicado": "http://www2.bmfbovespa.com.br/empresas/consbov/ArquivoComCabecalho.asp?motivo=&protocolo=679677&funcao=visualizar&site=B",
            
            value: "Valor": 0.370259884,
            adjusted_value: "ValorAjustado": 0.370259884,
    """
    instrument = models.ForeignKey(Instrument, related_name="dividends",
                on_delete=models.CASCADE)

   
    value = models.DecimalField('value', decimal_places=10, max_digits=20)
    adjusted_value = models.DecimalField('adjusted value', decimal_places=10, max_digits=20)
    
    

    def __str__(self):
        return f"{self.instrument.tckrSymb} - Category:{self.category}, ex-date:{self.ex_date}, R$ per Share: {self.value}"


    class Meta:
        unique_together = ('instrument', 'ex_date','category', 'event_date', 'value')
        verbose_name = 'Dividend'
        verbose_name_plural = 'Dividends'
        ordering = ['-ex_date']

class ProventoFII(BaseTimeModel):
    """
            instrument
            source_user
            ex_date
            payment_date
            reference_date
            value
            adjusted_value
            category
            details
            factor
            document_link
    """
    instrument = models.ForeignKey(Instrument, related_name="proventosFII",
                on_delete=models.DO_NOTHING)
    
    source_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    ex_date = models.DateField(
        'ex-date')  # precisa mesmo armazenar hora?
    payment_date = models.DateField(
        'payment date', blank=True, null=True)
    reference_date = models.DateField(
        'reference date', blank=True, null=True)
    value = models.DecimalField('value', decimal_places=9, max_digits=20, null=True)
    adjusted_value = models.DecimalField('adjusted value', decimal_places=9, max_digits=20, null=True)
    category = models.CharField('category', max_length=20)
    details = models.CharField('details', max_length=200, blank=True, null=True)
    factor = models.DecimalField('value', decimal_places=9, max_digits=20, null=True)
    document_link = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.instrument.tckrSymb} - Category:{self.category}, ex-date:{self.ex_date}, R$ per Share: {self.value}"

    class Meta:
        unique_together = ('instrument', 'ex_date','category', 'payment_date', 'value', 'reference_date')
        verbose_name = 'Dividend FII'
        verbose_name_plural = 'Dividends FII'
        ordering = ['-ex_date']

class Split(EventoAcao):
    """
            *instrument:"Empresa",
            *category:"Tipo": "DESDOBRAMENTO"/"GRUPAMENTO",
            *ex_date:"DataEx",
            *event_date: "DataEvento",
            *source_user:"Usuario"
            *document_link:"LinkComunicado",

            factor:"Fator",
            income_tax_price:"PrecoIR"
            fraction_price:"PrecoFracao"
            fraction_date: "DataFracao"
            details: "Detalhes"
    """
    instrument = models.ForeignKey(Instrument, related_name="splits", on_delete=models.CASCADE)
    factor = models.DecimalField('factor', decimal_places=9, max_digits=20, null=True, blank=True)
    income_tax_price = models.DecimalField('income tax price', decimal_places=9, max_digits=20, null=True, blank=True)
    fraction_price = models.DecimalField('fraction price', decimal_places=9, max_digits=20, null=True, blank=True)
    fraction_date = models.DateField('fraction date', blank=True, null=True)
    details = models.CharField('details', max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'Ticker:{self.instrument.tckrSymb} Date:{self.ex_date} Factor: {self.factor}'

    class Meta:
        unique_together = ('instrument', 'ex_date','category', 'event_date', 'factor', 'income_tax_price', 'fraction_date', 'fraction_price', 'details' ) 
        verbose_name = 'Split'
        verbose_name_plural = 'Splits'
        ordering = ['-ex_date']



class PriceHistory(BaseTimeModel):
    '''
    instrument, date, open, high, low, close, adj_close, volume, lastUpdate
    '''
    instrument = models.ForeignKey(Instrument, related_name="history",
                                   on_delete=models.CASCADE)
    date = models.DateField(
        'date')  # precisa mesmo armazenar hora?
    ## open é palavra protegida?
    open = models.DecimalField(
        'open', decimal_places=6, max_digits=20)
    high = models.DecimalField(
        'high', decimal_places=6, max_digits=20)
    low = models.DecimalField(
        'low', decimal_places=6, max_digits=20)
    close = models.DecimalField(
        'close', decimal_places=6, max_digits=20)
    adj_close = models.DecimalField(
        'adj_close', decimal_places=6, max_digits=20)
    volume = models.DecimalField(
        'volume', decimal_places=0, max_digits=20)  
    lastUpdate = models.DateTimeField('last update', blank=True, null=True)
    
    def __str__(self):
        return "{} {} R$ {}".format(self.date,self.instrument,self.adj_close)

    # def save(self, *args, **kwargs):
    #     if not self.open.isnull(): self.open = 0.
    #     if not self.high.isnull(): self.high = 0.
    #     if not self.low.isnull(): self.low = 0.
    #     if not self.close.isnull(): self.close = 0.
    #     if not self.adj_close.isnull(): self.adj_close = 0.
    #     if not self.volume.isnull(): self.volume = 0.
    #     if self.volume + self.adj_close + self.close + self.low + self.high + self.open == 0.: return False
    #     #     self.type = 0  # C
    #     # else:
    #     #     self.type = 1  # V
    #     # if self.total_costs == None:
    #     #     self.total_costs = 0

    #     super(PriceHistory, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('instrument', 'date',)
        verbose_name = 'Price History'
        verbose_name_plural = 'Price Histories'
        ordering = ['-date']



class Company(BaseTimeModel):
    instrument = models.ForeignKey(Instrument, related_name="company",
                                   on_delete=models.CASCADE)
    data = JSONField(default=dict)
    # display = JSONField()

    def __str__(self):
        return self.instrument.tckrSymb

    class Meta:
        unique_together = ('instrument', 'data',)
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['instrument']