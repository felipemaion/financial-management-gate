from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
import yfinance as yf
from core.models import DateTimeModel
# Create your models here.




class Instrument(DateTimeModel):
    tckrSymb = models.CharField('tckrSymb', max_length=20,unique=True)
    sgmtNm = models.CharField('sgmtNm', max_length=20, blank=True, null=True)
    mktNm = models.CharField('mktNm', max_length=20, blank=True, null=True)
    sctyCtgyNm = models.CharField("SctyCtgyNm",max_length=20, blank=True, null=True)
    isin = models.CharField('isin', max_length=20, blank=True, null=True)
    cFICd = models.CharField('cFICd', max_length=20, blank=True, null=True)
    crpnNm = models.CharField('crpnNm', max_length=20, blank=True, null=True)
    corpGovnLvlNm = models.CharField('corpGovnLvlNm', max_length=20, blank=True, null=True)
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
         ## This .SA is for South America (since the instruments are (for now) from SA). Future bug reported.
        stock = yf.Ticker(self.tckrSymb + ".SA")
        return stock.actions
    
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