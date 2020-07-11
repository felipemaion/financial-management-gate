from django.core.management.base import BaseCommand, CommandError
from wallet.models import Wallet, Moviment
from instrument.models import Instrument, Event, Dividend
from account.models import User

from .credential import get_url, get_header,get_cookies, DIVIDENDS_URL, SPLITS_URL

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
        self.url = get_url()
        self.site = requests.get(self.url)
        self.items = []
        self.data = {}
        self.display_keys = {}
        self.keys = []
        self.json_data = {}
        self.cdata = ""
        self.empresaID = None
        self.soup = self.get_data()
        
    def get_data(self):
        if self.empresaID == None:
            self.keys = []
            print(f"Procurando dados de {self.name}")
            self.soup = BeautifulSoup(self.site.text, "html.parser")
            self.cdata = self.soup.find(text=re.compile("CDATA"))
            # data = re.findall("\"Proventos\":{.*\:\{.*\:.*\}\}", self.cdata)[0]
            try: 
                empresaID_ = re.findall("\"Empresa\":{\"EmpresaID\":[^,]*", self.cdata)[0]
                self.empresaID = int(re.findall(r'\d+', empresaID_)[0])
                return self.empresaID
            except:
                print("Empresa não encontrada:" + self.name)
                pass

    def get_events(self, *args, **options):
        if self.empresaID == None: 
            self.get_data()
            if self.empresaID == None: return [None, None]
        events = [None, None]
        empresa_id = self.empresaID
       
        eventos0 = requests.post(url,
            data='{empresaID:' + str(empresa_id) + '}',
            headers=get_header(),
            cookies=get_cookies(),
        )
        try:
            company_content = eventos0.content
            json_p = json.loads(company_content)
            proventos = json.loads(json_p["d"])
            return proventos["Itens"]
        except:
            pass
            return None
        # 
        # # mglu = Instrument.objects.filter(tckrSymb="MGLU3")[0]
        

class Command(BaseCommand):
    help = 'Populacao dos eventos dos Instruments'
    
    

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Populando Eventos dos Instrumentos'))
        instruments = Instrument.objects.filter(sctyCtgyNm="SHARES")
        empresas = set([empresa.tckrSymb[:4] for empresa in instruments])
        maion = User.objects.filter(username="Maion")[0]
        proventos = []
        for empresa in empresas:
            cia = DataCompany(name=empresa)
            proventos, splits = cia.get_events()
            if proventos:
                for provento in proventos:
                    try: 
                        dividend, status = Dividend.objects.get_or_create(
                            instrument=Instrument.objects.filter(tckrSymb=provento["Acao"]["Codigo"])[0],
                            source_user = maion,
                            ex_date = convert_date(provento["DataEx"]),
                            event_date = convert_date(provento["DataPagamento"]),
                            accounting_date = convert_date(provento["DataContabil"]),
                            category = provento["Tipo"],
                            document_link = provento["LinkComunicado"],

                            value = provento["Valor"],
                            adjusted_value = provento["ValorAjustado"]
                        )
                        self.stdout.write(self.style.SUCCESS('Criado Provento para ' + str(dividend.instrument.tckrSymb) + ' da data ' + str(dividend.ex_date)))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING('Problema ao criar Evento: ' + str(dividend.instrument.tckrSymb) + ' da data ' + str(dividend.ex_date) + '\n' + str(e)))
                        continue