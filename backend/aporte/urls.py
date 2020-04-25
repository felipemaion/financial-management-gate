from django.urls import path

from .views import *

app_name = 'aporte'

urlpatterns = [
    path('',AporteListView.as_view(),name="aporte-list"),
    path('create',AporteCreateView.as_view(),name="aporte-create")
]
