from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
# Create your views here.
from .models import Aporte
from .forms import AporteForm

class AporteListView(ListView):
    model = Aporte
    template_name = "aportes.html"
    query_set = Aporte.objects.all()
    

class AporteCreateView(CreateView):
    model = Aporte
    template_name = "aporte_form.html"
    form_class = AporteForm
    success_url = reverse_lazy('aporte:aporte-list')