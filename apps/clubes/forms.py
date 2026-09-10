from django import forms
from .models import Ciclo

class CicloForm(forms.ModelForm):
    class Meta:
        #aqui campos extra 
        model = Ciclo
        fields = ['año', 'fecha_inicio', 'fecha_fin']