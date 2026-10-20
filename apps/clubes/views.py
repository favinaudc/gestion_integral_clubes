from django.shortcuts import render

# Create your views here.

class SharedFormMixin:
    template_name = 'clubes/form_template.html'  # Plantilla por defecto para los formularios