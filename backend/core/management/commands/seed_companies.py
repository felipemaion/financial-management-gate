from django.core.management.base import BaseCommand, CommandError
from instrument.models import Instrument, Company
import pandas as pd
from django.db.models import Q
from datetime import datetime
import yfinance as yf

import requests 
from bs4 import BeautifulSoup
import json
import re
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed_events





def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class DataCompany():
    def __init__(self, name):
        self.name = name
        self.url = "https://www.investsite.com.br/principais_indicadores.php?cod_negociacao={}".format(self.name)
        self.site = requests.get(self.url)
        self.items = []
        self.data = {}
        self.display_keys = {}
        self.keys = []
        self.json_data = {}
        self.getdata()

    def getdata(self):
        self.keys = []
        soup = BeautifulSoup(self.site.text, "html.parser")
        div = soup.find(id="mostradados_empresa")
        tables_list = div.find_all("table")
        # for c in range(len(tables_list)):
        for table in tables_list:
            lists = table.find_all("td")
            for lis in lists:
                try:
                    self.items.append(lis.contents[0])
                except:
                    self.items.append('-')
            contx = 0
            conty = 1
            while True:
            
                if conty >= len(self.items):
                    break
                else:
                    key, value = self.items[contx], striphtml(str(self.items[conty]))
                    new_key = self.clean_key(key)
                    # print("{}:{}".format(new_key, value))
                    self.display_keys[new_key] = key
                    self.keys.append(new_key)
                    self.data[new_key] = value                          
                    contx += 2
                    conty += 2
            self.items = []
        self.data["url"] = self.url 
        self.display_keys["url"] = "URL"   
        data = {"data":self.data, "display":self.display_keys}    
        self.json_data = json.dumps(data, ensure_ascii=False).encode("utf8").decode() 
        return self.json_data

    def clean_key(self, key):
        new_key = self.clean_string(key)
        return new_key

    def to_camel_case(self, key):
        words = key.split(' ')
        return words[0].lower() + ''.join(x.title() for x in words[1:])


    def clean_string(self, key):
        key = key.replace(".","").replace("s/","Sobre").replace("(","").replace(")","").replace("/"," ")
        translationTable = str.maketrans("éàèùâêîôûçõóíãáúü"+"éàèùâêîôûçõóíãáúü".upper(), "eaeuaeioucooiaauu"+"eaeuaeioucooiaauu".upper())
        key = key.translate(translationTable)
        return self.to_camel_case(key)

# class Company(DataCompany):
#     def __init__(self, name):
#         super(Company,self).__init__(name)
#         self.getdata()
#     def __str__(self):
#         return str(self.data)
       






class Command(BaseCommand):
    help = 'Populando Fundamentos dos Instrumentos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Populando Fundamentos dos Instrumentos'))
        instruments = Instrument.objects.all()
        assets = [instrument.tckrSymb for instrument in instruments]
        # TODO Testar código inválido.
        error_log = []
        for asset in assets:
            try:
                data = DataCompany(asset).getdata()
                instrument = Instrument.objects.filter(tckrSymb=asset)[0]
                company = Company.objects.get_or_create(instrument=instrument, data=data)
                self.stdout.write(self.style.SUCCESS('Populado Fundamentos de:' + asset))
            except Exception as e:
                self.stdout.write(self.style.ERROR('Não foi possível popular Fundamentos da Compania:' + asset + ' erro:' + str(e) ))
                pass
