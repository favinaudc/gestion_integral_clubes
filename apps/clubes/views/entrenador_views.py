from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, CreateView, DetailView, UpdateView
from apps.clubes.models import Entrenador
from apps.customauth.mixins import LoginRequiredMixinConMensaje
from ..mixins import SharedFormMixin
from ..forms import EntrenadorForm
from django.core.exceptions import PermissionDenied

class EntrenadorCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = Entrenador
    form_class = EntrenadorForm
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de crear un entrenador  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear entrenador'
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_volver'] = 'clubes:listar_entrenadores'  # URL para el botón de volver
        return context

class EntrenadorDetailView(LoginRequiredMixinConMensaje, DetailView):
    model = Entrenador
    template_name = 'clubes/entrenador/entrenador_detail.html'
    context_object_name = 'entrenador'  # Nombre del contexto para acceder a los entrenadores en la plantilla


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_volver'] = 'clubes:listar_entrenadores'  # URL para el botón de volver
        return context


class EntrenadorListView(LoginRequiredMixinConMensaje, ListView):
    model = Entrenador
    template_name = 'clubes/entrenador/entrenador_list.html'
    context_object_name = 'entrenadores'  # Nombre del contexto para acceder a los entrenadores en la plantilla 

    def get_queryset(self):
        entrenadores = Entrenador.objects.prefetch_related('club').all() 
        return entrenadores
         # Prefetch related para optimizar consultas

class EntrenadorUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = Entrenador
    form_class = EntrenadorForm
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de editar un entrenador 

    def dispatch(self, request, *args, **kwargs):
        # Aquí puedes agregar lógica adicional antes de procesar la solicitud
        if not request.user == self.get_object().usuario:
           raise PermissionDenied("No tienes permiso para editar este entrenador.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']= f'Editar entrenador'
        context['url_volver'] = 'home'
        return context
    

class EntrenadorDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = Entrenador
    template_name = 'clubes/entrenador_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista después de eliminar un entrenador   