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
    

    

    def amont_mais_10(self):
        # takes value inserted in the database
        print(self.date) # format 2019-01-01 year-month-day

        return self.amount + 10