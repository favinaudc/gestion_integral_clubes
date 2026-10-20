from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from apps.clubes.models import Entrenador
from django.views.generic import ListView
from django.views.generic import CreateView
from ..views.shared_views import SharedFormMixin
from ..forms import EntrenadorForm

class EntrenadorCreateView(SharedFormMixin, CreateView):
    model = Entrenador
    form_class = EntrenadorForm
   
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de crear un entrenador  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear entrenador'
        return context

class EntrenadorDetailView(ListView):
    model = Entrenador
    template_name = 'clubes/entrenador_detail.html'
    context_object_name = 'entrenadores'  # Nombre del contexto para acceder a los entrenadores en la plantilla

    def get_queryset(self):
        # Filtra los entrenadores por el ID del club proporcionado en la URL
        club = self.kwargs.get('club')
        return Entrenador.objects.filter(club=club)


class EntrenadorListView(ListView):
    model = Entrenador
    template_name = 'clubes/entrenador/entrenador_list.html'
    context_object_name = 'entrenadores'  # Nombre del contexto para acceder a los entrenadores en la plantilla 

    def get_queryset(self):
        entrenadores = Entrenador.objects.prefetch_related('club').all() 
        return entrenadores
         # Prefetch related para optimizar consultas

class EntrenadorUpdateView(SharedFormMixin, UpdateView):
    model = Entrenador
    form_class = EntrenadorForm
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de editar un entrenador 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']= f'Editar entrenador'
        return context

class EntrenadorDeleteView(DeleteView):
    model = Entrenador
    template_name = 'clubes/entrenador_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista después de eliminar un entrenador   