from django.db import models

import datetime
from .selic import corrigir_selic
import re # REALLY??
import json


# Create your models here.

class Aporte(models.Model):
    amount = models.DecimalField("Amount", max_digits=10, decimal_places=2)
    date = models.DateField("Date")
    final_date = models.DateField("Final Date",auto_now=False, auto_now_add=False,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def present_value(self, final_date=None):
        today = datetime.date.today()
        print(today)
        data_final = ""
        if final_date:
            data_final = final_date.strftime('%d/%m/%Y')
        else:
            if self.final_date > today:
                print("Aporte: {} - Data final {} maior que o dia de hoje {}.".format(self.amount, self.final_date, str(today.strftime('%d/%m/%Y')) ))
                data_final = today.strftime('%d/%m/%Y')
            else:
                data_final = self.final_date.strftime('%d/%m/%Y')

        selic = corrigir_selic(self.amount, self.date.strftime('%d/%m/%Y'), data_final)
        selic_real = re.search('(?<=\ )(.*?)(?=\ )', selic["valorCorrigido"]).group(1)
        return selic_real

    def amount_mais_selic(self):
        # takes value inserted in the database
        # print(self.date) # format 2019-01-01 year-month-day
        # print(self.final_date)
        return self.present_value()