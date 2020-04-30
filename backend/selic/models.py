from django.db import models
import datetime
from functools import reduce
import json
import requests
from decimal import Decimal



    

# Create your models here.
class Selic(models.Model):
    # Vou ter q fazer isso... fica muito lerdo pela API da net
    date = models.DateField("Date")
    daily_factor = models.DecimalField("Daily Fator", max_digits=11, decimal_places=10)

    def validate_unique(self):
        qs = Selic.objects.filter(date=self.date)
        if qs.filter(date=self.date).exists():
            print("Já existe")
            return False
        return True 

    def save(self, *args, **kwargs):
        if self.validate_unique():
            super(Selic, self).save(*args, **kwargs)

    def present_value(amount, initial_date, final_date=None):
        update_me()
        amount = Decimal(amount)
        today = datetime.date.today()
        if not final_date:
            final_date = today.strftime('%Y-%m-%d')
        qs = Selic.objects.filter(date__range=[initial_date, final_date]).values_list('daily_factor', flat=True)
        fator = reduce((lambda x,y: x*y), qs)
        # print(f"Data Inicial: {initial_date}, Data Final: {final_date}, Fator: {fator}")
        selic_real = amount * fator
        return round(selic_real,2)
    
    def update_me(self):
        update_me()



    def __str__(self):
        return "Data: {}, Fator Diário: {}".format(self.date, self.daily_factor)

    
    # objects = SelicManager()

        # mult = ""
        # if self.amount < 0:
        #     mult = "-"
        # selic = corrigir_selic(valor, self.date.strftime('%d/%m/%Y'), data_final)
        # selic_real = re.search('(?<=\ )(.*?)(?=\ )', selic["valorCorrigido"]).group(1)
        # return str(str(mult) + str(selic_real))

def update_me(): # sem self mesmo... chamado no View get_context_data
    try:
        last_info = Selic.objects.latest('date').date.strftime("%d/%m/%Y")
        print("Último dado no Sistema:", last_info)
        today = datetime.date.today().strftime("%d/%m/%Y")
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?dataInicial="+last_info+"&dataFinal="+today
        print(url)
        r = requests.get(url)
        print("Último dado no Servidor do Governo:", json.loads(r.content)[-1]['data'])
        if last_info == json.loads(r.content)[-1]['data']:
            print("Atualizado")
            return False
        #url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?dataInicial="+last_info+"&dataFinal="+today
        # input(url)
        #r = requests.get(url)
        populate_selic(json.loads(r.content))
        last_info = Selic.objects.latest('date')
    except:
        print("Algum erro ocorreu ao verificar banco de dados SELIC, atualizando tudo.")
        r = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados")
        populate_selic(json.loads(r.content))
        last_info = Selic.objects.latest('date')
    return last_info.date

def populate_selic(dados):
        for dado in dados:
            print("Atualizando:", dado)
            p = Selic(date=datetime.datetime.strptime(dado['data'],"%d/%m/%Y"), daily_factor=float(dado['valor'])/100+1)
            p.save()

# ta no aporte...


    