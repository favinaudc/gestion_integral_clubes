from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Ciclo

class CicloForm(forms.ModelForm):
    año = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu ciclo correspondiente...'
        }) )
    fecha_inicio = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                
            }) )
    fecha_fin = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                
            }) )
    class Meta:
        #aqui campos extra 
        model = Ciclo
        fields = ['año', 'fecha_inicio', 'fecha_fin']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar el FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Definir el Layout
        self.helper.layout = Layout(
            # Los 3 campos dentro de una misma Row divididos en 3 Columnas (col-md-4 cada una para repartir el espacio)
            Row(
                Column('año', css_class='form-group col-md-4 mb-3'),
                Column('fecha_inicio', css_class='form-group col-md-4 mb-3'),
                Column('fecha_fin', css_class='form-group col-md-4 mb-3'),
                css_class='row'
            ),
            # Botón verde (btn-success), texto en mayúsculas (text-uppercase) y centrado (text-center en un contenedor o clase de Bootstrap)
            # Nota: Agregamos una capa o clases utilitarias de Bootstrap para centrar el botón de forma limpia.
            Row(
                Column(
                    Submit('submit', 'GUARDAR CICLO', css_class='btn btn-success text-uppercase '),
                    css_class='col-md-6 mx-auto text-center mt-3' # 'mx-auto' centra la columna y 'w-100' hace que ocupe el ancho de esa columna central
                )
            )
        )