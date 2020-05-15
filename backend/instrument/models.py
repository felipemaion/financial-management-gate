from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
import yfinance as yf
from core.models import BaseTimeModel
# Create your models here.


class Instrument(BaseTimeModel):
    tckrSymb = models.CharField('tckrSymb', max_length=20, unique=True)
    sgmtNm = models.CharField('sgmtNm', max_length=20, blank=True, null=True)
    mktNm = models.CharField('mktNm', max_length=20, blank=True, null=True)
    sctyCtgyNm = models.CharField(
        "SctyCtgyNm", max_length=20, blank=True, null=True)
    isin = models.CharField('isin', max_length=20, blank=True, null=True)
    cFICd = models.CharField('cFICd', max_length=20, blank=True, null=True)
    crpnNm = models.CharField('crpnNm', max_length=20, blank=True, null=True)
    corpGovnLvlNm = models.CharField(
        'corpGovnLvlNm', max_length=20, blank=True, null=True)
    lastUpdate = models.DateTimeField('last update', blank=True, null=True)

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
            data = yf.download(self.tckrSymb + '.SA', date)
            return data['Adj Close'][0]
        except:
            return 0
    get_price.short_description = 'Price'
    get_price.admin_order_field = 'instrument__price'

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['-id']

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
        return 'SIMBOL:{} Date:{} Dividends: {} Stock Splits: {}' .format(
            self.instrument.tckrSymb,
            str(self.event_date),
            str(self.dividends),
            str(self.stock_splits))

    class Meta:
        unique_together = ('instrument', 'event_date',)
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-event_date']


class History(BaseTimeModel):
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

    def save(self, *args, **kwargs):
        if not self.open.isnumeric(): self.open = 0
        if not self.high.isnumeric(): self.high = 0
        if not self.low.isnumeric(): self.low = 0
        if not self.close.isnumeric(): self.close = 0
        if not self.adj_close.isnumeric(): self.adj_close = 0
        if not self.volume.isnumeric(): self.volume = 0
        if self.volume + self.adj_close + self.close + self.low + self.high + self.open = 0: return
        #     self.type = 0  # C
        # else:
        #     self.type = 1  # V
        # if self.total_costs == None:
        #     self.total_costs = 0

        super(Moviment, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('instrument', 'date',)
        verbose_name = 'History'
        verbose_name_plural = 'Histories'
        ordering = ['-date']