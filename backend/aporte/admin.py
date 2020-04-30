from django.contrib import admin
from .models import *


class AdminInstrument(admin.ModelAdmin):
    list_display = ["tckrSymb", "sgmtNm", "mktNm", "sctyCtgyNm", "isin", "cFICd", "crpnNm", "corpGovnLvlNm"] # aqui vc precisa colocar as colunas que vc quer ver
    search_fields = ["tckrSymb"]
    list_filter = ["sctyCtgyNm"]
 # listar por categoria Ex sexo nao sei o que tem de categoria por ai. Nesse aqui nada... pra falar a verdade algumas coisas aqui são bem inúteis (por hora...)
    # era isso? SENSACIONAL!
    # Boa... criei um mov la... agora vou pensar em como ver isso ai... e etc..
    # e o tipo C/V cara, não sei se é necessário. Se quantidade > 0 Compra, < 0 venda.
    # entao nao precisa vai ser uma verificacao 
    # #a gmoraa ss definir fica mais facil identificar
    # mais pro db fica mais facil saber se é compra ou venda mais 
    # tando faz se um IF nao faz dificuldade
    class Meta:
        verbose_name = "Admin Instrument"
        verbose_name_plural = "Admin Instruments"
        #ordering = ['tckrSymb']

class AdminMoviment(admin.ModelAdmin):
    list_display = ["wallet", "instrument", "date", "quantity","price"]
    exclude= ('type',)
# Register your models here. #red :)
admin.site.register([Aporte,Grupo, Ativo, TipoAtivo])
admin.site.register(Instrument, AdminInstrument)
admin.site.register(Moviment,AdminMoviment)

# Não queria ter q passar esse argumento ao criar o objto.. ehehe 
# Ok, então terei q colocar algum método para salvar isso.
# ?
# Para  colocar no db o C/V dependendo da qtd. 
# antes de salvar..
# nao vai precisar , vamo supor que vc registra 10 mov qtd 0 
# venda = mov.quantidade  = 0 so 
# isso÷

# entendi, mas ai eu tiro do db o C/V
#  sim pode tirar mais é com deixar descriminado no modelo com comentatio pra quem pegar saber o que é veda ou compra
# poe um comentario na classe 
# eu prefiro criar um metodo q antes de salvar, ve se qtd >0 e coloca 1 ou 0 (hehehe ja q é int)
# isso salva processamento na hora da busca...
# se fizer o mov.quant > 0 tem um comparativo a cada busca... certo?
# ideal é depois de salvar se o mov .... atribui 1 ou 0 C/V isso ? 
# SIM   
# exist os signals vou te mostrar

