from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from apps.customauth.mixins import LoginRequiredMixinConMensaje
from django.urls import reverse_lazy
from apps.clubes.models import Socio
from ..mixins import SharedFormMixin
from ..forms import SocioForm

class SocioCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = Socio
    form_class = SocioForm
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista de socios después de crear un socio      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear socio'
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_volver'] = 'clubes:listar_socios'  # URL para el botón de volver
        return context
class SocioDetailView(LoginRequiredMixinConMensaje, ListView):
    model = Socio
    template_name = 'clubes/socio_detail.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

    def get_queryset(self):
        # Filtra los socios por el ID del club proporcionado en la URL
        club = self.kwargs.get('club')
        return Socio.objects.filter(club=club)

class SocioListView(LoginRequiredMixinConMensaje, ListView):
    model = Socio
    template_name = 'clubes/socio/socio_list.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

class SocioUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = Socio
    form_class = SocioForm
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista de socios después de editar un socio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = f'Editar socio {self.object}'
        return context

class SocioDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = Socio
    template_name = 'clubes/socio/socio_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista después de eliminar un socio  