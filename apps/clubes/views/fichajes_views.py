from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from apps.customauth.mixins import LoginRequiredMixinConMensaje
from django.urls import reverse_lazy
from apps.clubes.models import Fichaje
from ..mixins import SharedFormMixin
from ..forms import FichajeForm
from django.urls import reverse

class FichajeCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = Fichaje
    form_class = FichajeForm
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de crear un fichaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear fichaje'
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_volver'] = 'clubes:detalles_fichaje'  # URL para el botón de volver
        return context

class FichajeDetailView(LoginRequiredMixinConMensaje, DetailView):
    model = Fichaje
    template_name = 'clubes/fichaje/fichaje_detail.html'
    context_object_name = 'fichaje'  # Nombre del contexto para acceder al fichaje en la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_volver'] = 'clubes:listar_fichajes'  # Cambia esto si tu URL de lista se llama diferente
        return context

class FichajeListView(LoginRequiredMixinConMensaje, ListView):
    model = Fichaje
    template_name = 'clubes/fichaje/fichaje_list.html'
    context_object_name = 'fichajes'  # Nombre del contexto para acceder a los fichajes en la plantilla

class FichajeUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = Fichaje
    form_class = FichajeForm
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de editar un fichaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar fichaje {self.object}'
        context['url_volver'] = 'clubes:listar_fichajes'  # Usamos la ruta limpia sin errores de PK
        return context

class FichajeDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = Fichaje
    template_name = 'clubes/fichaje_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista después de eliminar un fichaje