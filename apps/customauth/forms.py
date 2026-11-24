from typing import ClassVar

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from .models import Perfil, Usuario


class UsuarioExistenteForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Seleccionar Usuario",
    )


class NuevoUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("cuit_cuil", "email")
        widgets: ClassVar[dict] = {
            "cuit_cuil": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Sin guiones"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class NuevoPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("nombre", "apellido", "fecha_nacimiento", "telefono", "direccion")
        widgets: ClassVar[dict] = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("nombre", "apellido", "fecha_nacimiento", "telefono", "direccion")
        widgets: ClassVar[dict] = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("nombre", css_class="form-group col-6 mb-3"),
                Column("apellido", css_class="form-group col-6 mb-3"),
                css_class="row",
            ),
            Row(
                Column("fecha_nacimiento", css_class="form-group col-md-6 mb-3"),
                Column("telefono", css_class="form-group col-md-6 mb-3"),
                css_class="row",
            ),
            Row(
                Column("direccion", css_class="form-group col-md-6 mb-3"),
                css_class="row",
            ),
            Row(
                Column(
                    Submit(
                        "submit",
                        "GUARDAR PERFIL",
                        css_class="btn btn-success text-uppercase ",
                    ),
                    css_class="col-md-6 mx-auto text-center mt-3",
                )
            ),
        )
