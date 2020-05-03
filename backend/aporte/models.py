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


class DateTimeModel(models.Model):
    created_at = models.DateTimeField('created at', auto_now_add=True, blank=True)

    class Meta:
        abstract = True 



class Instrument(DateTimeModel):
    tckrSymb = models.CharField('tckrSymb', max_length=20,unique=True)
    sgmtNm = models.CharField('sgmtNm', max_length=20, blank=True, null=True)
    mktNm = models.CharField('mktNm', max_length=20, blank=True, null=True)
    sctyCtgyNm = models.CharField("SctyCtgyNm",max_length=20, blank=True, null=True)
    isin = models.CharField('isin', max_length=20, blank=True, null=True)
    cFICd = models.CharField('cFICd', max_length=20, blank=True, null=True)
    crpnNm = models.CharField('crpnNm', max_length=20, blank=True, null=True)
    corpGovnLvlNm = models.CharField('corpGovnLvlNm', max_length=20, blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['-id']
    
    def __str__(self):
        return "{}: {}".format(self.tckrSymb, self.crpnNm)

class Moviment(DateTimeModel):

    TYPE_CHOICES = (
        (0, 'COMPRA'),
        (1, 'VENDA'),
    )
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    type = models.IntegerField('type', choices=TYPE_CHOICES, blank=True , null=True)
    quantity = models.IntegerField('quantity')
    total_investment = models.DecimalField('price', decimal_places=2, max_digits=10)
    total_costs = models.DecimalField('costs', decimal_places=2, max_digits=10)
    date = models.DateField('date')
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.type = 0
        else:
            self.type = 1
                
        super(Moviment,self).save(*args,**kwargs) #	

# to digitando e parei
# quer dizer eu acho que tava modelando errado voce pode colocar a carteia diretamento no movimento j
#a que nao vai ter nenhum daddo entre os 2
# Isso  minha vez... haha
# que loko nao foi haahha

# é porque ele sempre vai chamar o save
# @receiver(post_save, sender=Moviment) # iaew O q vc fez? so passei esse parametro created que verifica se o obj esta sendo criado. e qm está passando esse parametro? E eum chama esse save_instrument? 
# # quem passa é o decorator 
# # pode ser assim tbm

#     def save_instrument(sender, instance, created, **kwargs):
#         if created:
#             instance.chamafuncao()

# acho que ta pronto 
# ?? seguinte vou fazer aqui StoryUser

#1 quando o usuario for registrar o movimento ele ja deve ter uma carteira registrada OK?ok
#2 quanto ele for registrar um movimento ele tem que interir um instrumento, correto?
#3 caso o instrumento que ele estiver registrando no exista en nossa base seria interessante registrar antes?? 
#4 o usuario so vai poder fazer um movimento do instrumento que esteja registrado no sistema.



# hummm ok... (apesar de ter q limpar os instrumentos heehh go go go)
# Sim..., ele mesmo registra ou pede para o administrator criar? Cara... admin. se deixar por conta do usuario ele caga tudo:D hhhaha é
# Como vc subiria o csv para o db de instrumento? já filtrando os campos?


# user_carteira;
# instrumento;

''''
Atividade do usuario
# movimento =  {
    
    # user_carteira,
    instrumento,
    tipo (COMPRA/VENDA)
    quantidade,
    preco
    custos
    data
}
'''
# o relacionamento é da seguinte maneira 
# quando o usuario/auto cria o movimento 
# esse movimento vai ter o id vamos chamar aqui de mov_user_id

# mov_user_id = :ex 1 

# ao criar esse mov em seguida vai ser criado uma tabela_pivot com a user_carteira 

# assim MovimentWallet.objects.create(
#       moviment=mov_user_id,
#       wallet=user_carteira
# )
# cosegue entender? 
# isso é o que vai garantir que esse movimento é dessa carteira e é isso.

# acho q entendi... pq vc está pegando  omov_user_id de outro lugar, é isso? Por isso q garante?
# o mov_user_id é o id que acabou de ser criado pelo usuario ou no automativo seja como for

# acho q não captei.. ahahah
# faz disso uma api e vamos tentar criar algo no terminal... da?
# se eu for fazer api vai complicar o seu entendimento porque nao tem haver com outra? :D voce tem que entender o relacionamento da esttrutura
# eu entendi o relacionamento... só não entendi o q vai garantir que o mov não seja colocado em outra carteira haaha
# vou da um exemplo aqui 


# no ato do usuario enviar uma requisicao
# é enviado junto o os dados dele pelo TOKEN(unico dele)



# user_loged = ALISON

# carteira_enviada = 1 ou XP_INVEST
# # Wallet Modelo definido no backend
# carteira = Wallet.objects.get(id=carteira_enviada, user=user_loged)

# if carteira:
#     print('dono da carteira')
# else:
#     print('nao é dono')
# se ele encontrar é porque a carteira é desse usuario
