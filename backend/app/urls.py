"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path,include

# urlpatterns = [
#     path('',include('aporte.urls',namespace="aporte")),
#     path('admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.urls import path, include

# aqui tem duas rotas em branco no caso root na primeira rota ele vai dar o get 
# e nao passa para segunda então tem que nomear
# então a rota vai ficar localhost:port/selic/exemplo testa ai

urlpatterns = [
    path('',include('aporte.urls',namespace="aporte")),
    path('selic/',include('selic.urls',namespace="selic")),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]