from django import forms
from .models import Usuario, Perfil

class UsuarioExistenteForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Seleccionar Usuario"
    )

class NuevoUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cuit_cuil', 'email']
        widgets = {
            'cuit_cuil': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sin guiones'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class NuevoPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }