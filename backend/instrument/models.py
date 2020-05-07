from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
import yfinance as yf
# Create your models here.


class DateTimeModel(models.Model):
    created_at = models.DateTimeField('created at', auto_now_add=True, blank=True)

    class Meta:
        abstract = True 


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

    def price(self, inital_date=datetime.now(), final_date=datetime.now()):
        return yf.download(self.tckrSymb + ".SA", inital_date, final_date)

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['-id']
    
    def __str__(self):
        return "{}: {}".format(self.tckrSymb, self.crpnNm)