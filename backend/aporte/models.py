from django.db import models
from functools import reduce
import datetime
# from datetime import timedelta
#from .selic import corrigir_selic
from decimal import Decimal
from selic.models import Selic
from wallet.models import Wallet
from django.db.models.signals import post_save
from django.dispatch import receiver
# Extend User: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html


# Create your models here.
# CHORO?? hahaha  ??? Esquece... vamos para a parte de cadastrar o movimento de ativos na carteira.
# API.

#  Vamo fazer os modelos aqui depois refatoramos
class Grupo(models.Model):
    name = models.CharField(max_length=60, unique=True)

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
                data_final = (self.final_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        valor = self.amount
        # qs = Selic.objects.filter(date__range=[self.date, data_final]).values_list('daily_factor', flat=True)
        # fator = reduce((lambda x,y: x*y), qs)
        # selic_real = valor * fator
        #### SERA ??? # 
        selic_real = Selic.present_value(valor,self.date, data_final)
        #### talvez consumir a API?
        return round(selic_real,2)
        
    def __str__(self):
        return "Grupo: {}, Amount: {}, Data: {}".format(self.grupo, self.amount, self.date)

class TipoAtivo(Grupo):
    tipo = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return "{}:{}".format(self.name, self.id)

class Ativo(Aporte):
    None





### Usuário
# Carteira:
#   Instituições.
#       Aportes em Instituições. # Valor do Aporte, Data do Aporte, {Valor Corrigido pela Selic, Valor Total}
#       Compra/Venda de Ativos:
#           Dinheiro na Instituição. # Saldo na conta da Instituição
#           Ações na Instituição. # Codigo, Data de Compra/Venda, Quantidade, Preço de Compra/Venda, Custos, Total, {Valor Atual, Valor Corrigido pela Selic}
#           Fundos Imobiliários (...). # Idem.
#           Fundos (...)
#           Tesouro Direto.
#           Duplicatas/Títulos. # 
#           Imóveis.
#           Forex.
#           Etc.


# Tipo de Aporte (Instituição, Ativos, Passivos, etc.)


### Tentando fazer uma API para retornar somente valor corrigido da SELIC:

# class Corrige(models.Model):
#     def __init__(self, amount, date, final_date):
#         self.amount = amount
#         self.date = date
#         self.final_date = final_date

#     def present_value(self, final_date=None):
#         today = datetime.date.today()
#         # print(today)
#         data_final = ""
#         if not self.final_date:
#             final_date = today
#         if final_date:
#             data_final = final_date.strftime('%Y-%m-%d')
#         else:
#             if self.final_date > today:
#                 print("Aporte: {} - Data final {} maior que o dia de hoje {}.".format(self.amount, self.final_date, str(today.strftime('%d/%m/%Y')) ))
#                 data_final = today.strftime('%Y-%m-%d')
#             else:
#                 data_final = (self.final_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
#         valor = self.amount
#         qs = Selic.objects.filter(date__range=[self.date, data_final]).values_list('daily_factor', flat=True)
#         fator = reduce((lambda x,y: x*y), qs)
#         selic_real = valor * fator
#         return round(selic_real,2)


# Instrumento Pertence ao movimento vamos vazer o modelo de Instrumento
# Começa do zero num novo arquivo. # vai ficar melhor pra vc entender so esquece o que estar acima...
# Ok \o/
# Vou colar aqui os atributos que definimos la


# tckrSymb(Unique)
# crpnNm
# sgmtNm
# mktNm
# mctyCtgyNm
# ISIN
# corpGovnLvlNm
# cFICd

# nao sei o que eles queren dizer voce pode ir traduzindo ai :D
# Tudo é Texto?

# Cara na vdd eu sei mais ou menos... bem pra menos.. tudo texto. São coisas para identificar o Ativo Globalmente.
# tudo pode ser brano ou nulo?

# Não.. tckrSymb nao... mktNm tb não.
# OK

# Deixa eu abrir a tabela aqui... guenta hahah ...vo buscar cafe

# Cara, sgmtNm por exemplo, é uma classificação. Fica como string? pode ser se for muitas classificacoes 
# melhor ser uma tabela relacionada ex: sexo é F/M já profissao sao muitas, vamo fazer como string
#  Vamo pro moveimento

