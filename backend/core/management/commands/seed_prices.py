from django.core.management.base import BaseCommand, CommandError
from instrument.models import Instrument, PriceHistory
import pandas as pd
from django.db.models import Q
from datetime import datetime
import yfinance as yf

# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed_events


class Command(BaseCommand):
    help = 'Populacao dos eventos dos Instruments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Populando Preços de alguns Instrumentos'))

        # assets = ["ABCB4","AMZO34","ARZZ3","BBAS3","BRCR11","BRPR3","CIEL3","CSAN3","CYRE3","EZTC3","FAMB11B","FIGS11","FLRY3",
        # "GGRC11","GRND3","HGBS11","HGRE11","HGTX3","IRBR3","ITSA4","ITSA4","ITUB3","JHSF3","KEPL3","LCAM3","LEVE3","MBRF11","MELI34",
        # "MGLU3","MRVE3","MXRF11","PETR4","PETR4","PORD11","PRIO3","PRIO3","RADL3","RBBV11","RBGS11","RBRF11","RNGO11","SAPR4","SDIL11",
        # "SGPS3","SMAL11","SQIA3","TAEE11","TIET11","TRPL4","VIVA3","VVAR3","XPCM11","XPLG11","XPML11","ABEV3","FEXC11","KNRI11","RENT3",
        # 'ALSO3', 'BEEF3', 'HBOR3', 'JPSA3', 'LCAM3', 'PNVL3', 'SQIA3', 'STBP3']
        assets = ['PNVL3','BEEF3']
        # TODO Testar código inválido.
        error_log = []
        assets = [asset + ".SA" for asset in assets]
        try:
            ### TODO utilizar o PriceHistory para armazenar e pegar as info.
            print("Getting ONLINE Data for Assets:", assets)
            data = yf.download(assets, start="2010-01-01", end=datetime.now(), period="1d", group_by="Ticker")
            
        except:
            print("Error getting Online Data.")
        # try:
        print("Trying to populate PriceHistory with data:")
        size = len(assets)
        for i, asset in enumerate(assets):
            print("({}/{}):{}".format(i,size-1,asset))
            instrument = Instrument.objects.filter(tckrSymb=asset[:-3])[0]
            # data[asset].fillna(0)
            for date, info in data[asset].iterrows():
                info = info.dropna(axis='rows')
                if not info.empty:
                    # print(instrument,date,info['Open'],info['Close'],info['High'],info['Low'],info['Adj Close'],info['Volume'])
                    try:
                        PriceHistory = PriceHistory.objects.get_or_create(
                            instrument=instrument,
                            date=date,
                            open=info['Open'],
                            high=info['High'],
                            low=info['Low'],
                            close=info['Close'],
                            adj_close=info['Adj Close'],
                            volume=info['Volume'],
                            )
                        # print("\tNew PriceHistory added for", instrument)
                    except Exception as error:
                        print("Falha no ativo:{}\n{}".format(asset,error))
                        pass
                        # Sério... acho q tô pulando errado o ativo...
                        # break
        self.stdout.write(self.style.SUCCESS(
        'Vixe... deu certo.. populou preços'))
        # except:
        #     print("Error trying to populate PriceHistory")
        #     pass
        


    #         instrument = models.ForeignKey(Instrument, related_name="PriceHistory",
    #                                on_delete=models.CASCADE)
    # date = models.DateTimeField(
    #     'date')  # precisa mesmo armazenar hora?
    # ## open é palavra protegida?
    # open = models.DecimalField(
    #     'open', decimal_places=6, max_digits=20)
    # high = models.DecimalField(
    #     'high', decimal_places=6, max_digits=20)
    # low = models.DecimalField(
    #     'low', decimal_places=6, max_digits=20)
    # close = models.DecimalField(
    #     'close', decimal_places=6, max_digits=20)
    # adj_close = models.DecimalField(
    #     'adj_close', decimal_places=6, max_digits=20)
    # volume = models.DecimalField(
    #     'volume', decimal_places=0, max_digits=20)  