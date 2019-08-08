from django.db import models
from functools import reduce
import datetime
# from datetime import timedelta
from .selic import corrigir_selic
import re # REALLY??
import json
import csv
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

    def update_me():
        try:
            last_info = Selic.objects.latest('date').date.strftime("%d/%m/%Y")
            print(last_info)
            today = datetime.date.today().strftime("%d/%m/%Y")
            if today == last_info:
                print("Atualizado")
                return
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?dataInicial="+last_info+"&dataFinal="+today
            # input(url)
            r = requests.get(url)
            populate_selic(json.loads(r.content))
            last_info = Selic.objects.latest('date')
        except:
            r = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados")
            populate_selic(json.loads(r.content))
            last_info = Selic.objects.latest('date')
        return last_info.date

    def __str__(self):
        return "Data: {}, Fator Diário: {}".format(self.date, self.daily_factor)


def populate_selic(dados):
        for dado in dados:
            print("Atualizando:", dado)
            p = Selic(date=datetime.datetime.strptime(dado['data'],"%d/%m/%Y"), daily_factor=float(dado['valor'])/100+1)
            p.save()


class Grupo(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return "{}:{}".format(self.name, self.id)

class Aporte(models.Model):
    amount = models.DecimalField("Amount", max_digits=10, decimal_places=2)
    date = models.DateField("Date")
    final_date = models.DateField("Final Date",auto_now=False, auto_now_add=False,null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    grupo  = models.ForeignKey(Grupo,on_delete=models.CASCADE)

    def present_value(self, final_date=None):
        today = datetime.date.today()
        # print(today)
        data_final = ""
        if not self.final_date:
            final_date = today
        if final_date:
            data_final = final_date.strftime('%Y-%m-%d')
        else:
            if self.final_date > today:
                print("Aporte: {} - Data final {} maior que o dia de hoje {}.".format(self.amount, self.final_date, str(today.strftime('%d/%m/%Y')) ))
                data_final = today.strftime('%Y-%m-%d')
            else:
                data_final = self.final_date.strftime('%Y-%m-%d')
        valor = self.amount
        qs = Selic.objects.filter(date__range=[self.date, data_final]).values_list('daily_factor', flat=True)
        fator = reduce((lambda x,y: x*y), qs)
        selic_real = valor * fator
        return round(selic_real,2)
        # mult = ""
        # if self.amount < 0:
        #     mult = "-"
        # selic = corrigir_selic(valor, self.date.strftime('%d/%m/%Y'), data_final)
        # selic_real = re.search('(?<=\ )(.*?)(?=\ )', selic["valorCorrigido"]).group(1)
        # return str(str(mult) + str(selic_real))

    def amount_mais_selic(self):
        # takes value inserted in the database
        # print(self.date) # format 2019-01-01 year-month-day
        # print(self.final_date)
        return self.present_value()

    def __str__(self):
        return "Grupo: {}, Amount: {}, Data: {}".format(self.grupo, self.amount, self.date)