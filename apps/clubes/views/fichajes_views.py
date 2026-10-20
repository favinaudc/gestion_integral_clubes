from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from apps.clubes.models import Fichaje
from django.views.generic import DeleteView
from ..views.shared_views import SharedFormMixin
from ..forms import FichajeForm

class FichajeCreateView(SharedFormMixin, CreateView):
    model = Fichaje
    form_class = FichajeForm
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de crear un fichaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear fichaje'
        return context

class FichajeDetailView(ListView):
    model = Fichaje
    template_name = 'clubes/fichaje_detail.html'
    context_object_name = 'fichajes'  # Nombre del contexto para acceder a los fichajes en la plantilla

    def get_queryset(self):
        # Filtra los fichajes por el ID del socio proporcionado en la URL
        socio = self.kwargs.get('socio')
        return Fichaje.objects.filter(socio=socio)
        
class FichajeListView(ListView):
    model = Fichaje
    template_name = 'clubes/fichaje/fichaje_list.html'
    context_object_name = 'fichajes'  # Nombre del contexto para acceder a los fichajes en la plantilla

class FichajeUpdateView(SharedFormMixin, UpdateView):
    model = Fichaje
    form_class = FichajeForm
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de editar un fichaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar fichaje {self.object}'
        return context

class FichajeDeleteView(DeleteView):
    model = Fichaje
    template_name = 'clubes/fichaje_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista después de eliminar un fichaje