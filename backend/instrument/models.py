from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
import yfinance as yf
from core.models import BaseTimeModel
# Create your models here.


class Event(DateTimeField):


class Instrument(BaseTimeModel):
    tckrSymb = models.CharField('tckrSymb', max_length=20,unique=True)
    sgmtNm = models.CharField('sgmtNm', max_length=20, blank=True, null=True)
    mktNm = models.CharField('mktNm', max_length=20, blank=True, null=True)
    sctyCtgyNm = models.CharField("SctyCtgyNm",max_length=20, blank=True, null=True)
    isin = models.CharField('isin', max_length=20, blank=True, null=True)
    cFICd = models.CharField('cFICd', max_length=20, blank=True, null=True)
    crpnNm = models.CharField('crpnNm', max_length=20, blank=True, null=True)
    corpGovnLvlNm = models.CharField('corpGovnLvlNm', max_length=20, blank=True, null=True)
    lastUpdate = models.DateTimeField('last update', blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True, blank=True)

    def history(self):
        return yf.download( # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = self.tckrSymb + ".SA",  ## This .SA is for South America (since the instruments are (for now) from SA). Future bug reported.

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "ytd",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
        )

    def events(self):
         ## This .SA is for South America (since the instruments are (for now) from SA). 
        #  Future bug reported.
        stock = yf.Ticker(self.tckrSymb + ".SA")
        return stock.actions

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