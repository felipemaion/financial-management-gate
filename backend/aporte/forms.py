from django import forms 
from .models import Aporte


class AporteForm(forms.ModelForm):
    
    class Meta:
        model = Aporte
        fields = '__all__'
        widgets = {
            'date' : forms.TextInput(attrs={'type': 'date'}),
            'final_date':forms.TextInput(attrs={'type': 'date'}),
        }
