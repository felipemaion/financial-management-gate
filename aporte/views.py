from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
# Create your views here.
from .models import Aporte#, Selic
from .forms import AporteForm
from selic.models import Selic


class AporteListView(ListView):
    model = Aporte
    template_name = "aportes.html"
    query_set = Aporte.objects.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #busca a Selic 
        Selic.update_me()
        return context
    

class AporteCreateView(CreateView):
    model = Aporte
    template_name = "aporte_form.html"
    form_class = AporteForm
    success_url = reverse_lazy('aporte:aporte-list')