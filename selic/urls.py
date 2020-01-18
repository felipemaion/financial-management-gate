from django.urls import path
from .views import *

app_name = 'selic'

# aqui no urls.py é obrigatorio essa constante urlpatterns que é definido as 
# rotas cada path.. Exemplo é uma classe que extende de APIView
# Quanto voce bater na rota exemplo vai ter retornar
# a classe

urlpatterns = [
    path('', Corrige.as_view(),name='corrige')
]


# urlpatterns = [
#     path('',AporteListView.as_view(),name="aporte-list"),
#     path('create',AporteCreateView.as_view(),name="aporte-create")
# ]

# Url pattern obrigatorio