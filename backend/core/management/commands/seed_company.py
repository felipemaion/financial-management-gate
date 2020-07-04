from django.core.management.base import BaseCommand, CommandError
from instrument.models import Instrument, Company
import pandas as pd
from django.db.models import Q
from datetime import datetime
import yfinance as yf

# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed_events


class Command(BaseCommand):
    help = 'Populancao Preços de instrumentos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Populando Preços de alguns Instrumentos'))
        instruments = Instrument.objects.all()
        assets = [instrument.tckrSymb for instrument in instruments]
        # TODO Testar código inválido.
        error_log = []
        assets = [asset + ".SA" for asset in assets]
        try:
            ### TODO utilizar o PriceHistory para armazenar e pegar as info.
            print("Getting ONLINE Data for Assets:", assets)
            data = yf.download(assets, start="2020-01-01", end=datetime.now(), period="1d", group_by="Ticker")
            
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
                        history = PriceHistory.objects.get_or_create(
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
        'Vixe... deu certo.. populou as companias'))
