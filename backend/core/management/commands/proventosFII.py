from django.core.management.base import BaseCommand, CommandError
from wallet.models import Wallet, Moviment
from instrument.models import Instrument, Event, Dividend, Split
from account.models import User

from .credentialFII import get_url, get_header,get_cookies, FII_URL

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
        