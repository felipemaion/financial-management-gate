from django.core.management.base import BaseCommand, CommandError
from wallet.models import Wallet, Moviment
from instrument.models import Instrument, Event
import pandas as pd
from django.db.models import Q

# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed_events


class Command(BaseCommand):
    help = 'Populacao dos eventos dos Instruments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Populando Eventos dos Instrumentos'))
		# ta errado demais. Ahahah percebi.. como é o certo? Usando o Q?
        query = Q(sgmtNm="CASH", Q.AND)
        query.add(Q(sctyCtgyNm="SHARES"), Q.OR)
        query.add(Q(sctyCtgyNm="UNIT"), Q.OR)
        query.add(Q(sctyCtgyNm="FUNDS"), Q.OR)
		
        instruments = Instrument.objects.all().filter(query)

        for instrument in instruments:
            # Busca events relacionados ao instrument por yfinance

            events_origin = instrument.populate_events()
            # o try vai ficar aqui mesmo

            try:
                if not events_origin.empty:
                    for index, event in events_origin.iterrows():  # como pega apenas a data (id) da scrita no terminal
                        Event.objects.get_or_create(
                            instrument=instrument,
                            event_date=index.strftime("%Y-%m-%d"),
                            dividends=event['Dividends'],
                            stock_splits=event['Stock Splits']
                        )
                        self.stdout.write(self.style.SUCCESS(
                            'Criado'))
                        )
                        self.stdout.write(self.style.SUCCESS(
                            'Criado'))

            except:
                print('error')
                pass
                # vendo ai, sempre é pra testar antes de inserir. Sim!
                # nao ta iterando pq sera? Deve ter Instruments que não tem eventos
                # ev = Event.objects.create(
                #     instrument=instrument,
                #     event_date=index.split(' ')[0],
                #     dividends=event['Dividends'],
                #     stock_splits=event['Stock Splits']
                #     )
            # Sim
                # primeiro vamo iterar depois criamos ? Pq? testar se ele consegue busacar tudo...
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

                # sao 3 colunas
                # Dividends, Date, Stock Splits entendi
                # try:
                # 	# create event
                # 	event = Event.objects.create(
                # 		instrument=instrument,
                # 		event_date=instrument.data,
                # 		dividends=instrument.dividends
                # 	)
                # except Exception as error:
                # 	pass
