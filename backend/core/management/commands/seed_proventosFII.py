from django.core.management.base import BaseCommand, CommandError
from wallet.models import Wallet, Moviment
from instrument.models import Instrument, ProventoFII
from account.models import User

from .credentialFII import get_url, get_header,get_cookies, PROVENTOS_FII_URL, EVENTOS_FII_URL

import requests 
from bs4 import BeautifulSoup
import json
import re
import datetime 

def convert_date(date_str):
    if date_str:
        date = int(re.findall('\d+', date_str )[0])  
        return datetime.datetime.fromtimestamp(date/1000.0)
    return None

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class DataCompany():
    def __init__(self, name):
        self.name = name
        self.url = get_url(self.name)
        self.site = requests.get(self.url)
        self.items = []
        self.data = {}
        self.display_keys = {}
        self.keys = []
        self.json_data = {}
        self.cdata = ""
        self.fundoID = None
        self.soup = self.get_data()
        
    def get_data(self):
        if self.fundoID == None:
            self.keys = []
            print(f"Procurando dados de {self.url}")
            self.soup = BeautifulSoup(self.site.text, "html.parser")
            self.cdata = self.soup.find(text=re.compile("CDATA"))
            # data = re.findall("\"provents\":{.*\:\{.*\:.*\}\}", self.cdata)[0]
            try: 
                # fundoJSON = {"Fundo":{"FundoID":87
                fundoID_ = re.findall("\"Fundo\":{\"FundoID\":[^,]*", self.cdata)[0]
                self.fundoID = int(re.findall(r'\d+', fundoID_)[0])
                return self.fundoID
            except:
                print("Fundo não encontrado:" + self.name)
                return None

    def get_request(self, url):
        if self.fundoID == None: 
            self.get_data()
            if self.fundoID == None: return None
        data = '{fundoID:' + str(self.fundoID) + '}'
        req = requests.post(url, data=data, headers=get_header(self.name), cookies=get_cookies(),)
        try:
            content = req.content
            return content
        except Exception as e:
            print(f"Erro ao requisitar fundo: {self.name} - {e}")
            return None

    def get_events(self, *args, **options):
        events = [None, None]
        events = [self.get_request(PROVENTOS_FII_URL), self.get_request(EVENTOS_FII_URL)]
        if events == [None, None]: return [None, None]
        try:
            # company_content = [ [dividends.content, splits.content] for dividends, splits in events]
            # print(company_content)
            [json_proventos, json_events] = [json.loads(events[0]), json.loads(events[1])]
            proventos, eventos = [json.loads(json_proventos["d"]), json.loads(json_events["d"])]
            return [proventos["Proventos"], eventos["Items"]]
        except Exception as e:
            print(f"Erro ao pegar eventos de {self.name}: {e} ")
            print(events)
            return [None, None]
        # 
        # # mglu = Instrument.objects.filter(tckrSymb="MGLU3")[0]
        

class Command(BaseCommand):
    help = 'Populacao dos eventos dos Instruments'
    
        
    def save_splits(self, instrument, split, source_user):
        self.errors = []
        try:
            dividend, _ = Split.objects.get_or_create(
                instrument=instrument,
                category = split["Tipo"],
                ex_date = convert_date(split["DataEx"]),
                event_date = convert_date(split["DataEvento"]),
                source_user = source_user,
                document_link = split["LinkComunicado"],

                factor = split["Fator"],
                income_tax_price = split["PrecoIR"],
                fraction_price = split["PrecoFracao"],
                fraction_date = convert_date(split["DataFracao"])
            )
            self.stdout.write(self.style.SUCCESS(f'Criado split para {dividend.instrument.tckrSymb} com data {dividend.ex_date}'))
        except Exception as e:
            # print(provent)
            self.errors.append([instrument.tckrSymb, convert_date(split["DataEx"])])
            self.stdout.write(self.style.ERROR(f'\tProblema ao criar Split da {instrument} com data {convert_date(split["DataEx"])} \n {e}'))
            pass
        finally:
            return self.errors


    def get_errors(self):
        return self.errors

    def handle(self, *args, **options):
        self.errors = []
        self.stdout.write(self.style.SUCCESS(
            'Populando Eventos dos Instrumentos Fundos Imobiliários'))
        instruments = Instrument.objects.filter(sctyCtgyNm="FUNDS")
        fundos = set([fundo.tckrSymb for fundo in instruments])  # ['MGLU', 'BIDI', 'PNVL'] # AS CASCUDAS! Problema ao criar Split da QUAL3, RAIL3, BBSE3 (problema com Amortização)
        maion = User.objects.filter(username="Maion")[0]
        provents = []
        for fundo in fundos:
            cia = DataCompany(name=fundo)
            provents, splits = cia.get_events()
            if provents:
                for provent in provents:
                    # print(provent)
                    try: 

                        provento, _ = ProventoFII.objects.get_or_create(
                            instrument=Instrument.objects.filter(tckrSymb=fundo)[0],
                            source_user=maion,
                            ex_date= convert_date(provent["DataEx"]),
                            payment_date=convert_date(provent["DataPagamento"]),
                            reference_date=convert_date(provent["DataReferencia"]),
                            value= provent["Valor"],
                            adjusted_value=provent["ValorAjustado"],
                            category=provent["Tipo"],
                            details=provent["Detalhes"],
                            factor=provent["Fator"]

                        )
                        #TODO Crear o modelo para proventos e eventos de FII. Popular.
                        # {'ProventoID': 24856, 
                        # 'DataPagamento': '/Date(1594695600000)/', 
                        # 'DataReferencia': '/Date(1594090800000)/', 
                        # 'DataEx': '/Date(1594177200000)/', 
                        # 'Valor': 0.569359, 
                        # 'ValorAjustado': 0.569359, 
                        # 'Tipo': 1, 
                        # 'Detalhes': None, 
                        # 'Fator': None, 
                        # 'SubscricaoID': None}


                        # dividend, _ = Dividend.objects.get_or_create(
                        #     instrument=Instrument.objects.filter(tckrSymb=provent["Acao"]["Codigo"])[0],
                        #     source_user = maion,
                        #     ex_date = convert_date(provent["DataEx"]),
                        #     event_date = convert_date(provent["DataPagamento"]),
                        #     accounting_date = convert_date(provent["DataContabil"]),
                        #     category = provent["Tipo"],
                        #     document_link = provent["LinkComunicado"],

                        #     value = provent["Valor"],
                        #     adjusted_value = provent["ValorAjustado"]
                        # )
                        self.stdout.write(self.style.SUCCESS(f'Criado Provento para {provento.instrument.tckrSymb} da data {provento.ex_date}'))
                    except Exception as e:
                        # print(provent)
                        self.stdout.write(self.style.WARNING(f'\tProblema ao criar Dividend da {fundo}  com data {convert_date(provent["DataEx"])} \n{e}'))
                        continue
            # if splits:
                
            #     for split in splits:
            #         # def guess_instrument(fundo):
            #         # 
            #         instruments = Instrument.objects.filter(tckrSymb__icontains=fundo)
            #         if len(instruments) > 1:
            #             # Get from yFinances the best guess. TODO (1/Fator) ???
            #             y_events = Event.objects.filter(instrument__tckrSymb__icontains=fundo, stock_splits__exact=split["Fator"]) 
            #             for event in y_events:
            #                 self.save_splits(instrument=event.instrument, split=split, source_user=maion)
            #         else:
            #             instrument = instruments[0]
            #             self.save_splits(instrument=instrument, split=split, source_user=maion)
        return self.errors
