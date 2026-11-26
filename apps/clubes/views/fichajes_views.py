from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from apps.customauth.mixins import (
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
)
from django.urls import reverse_lazy
from apps.clubes.models import Fichaje, Socio
from ..mixins import SharedFormMixin
from ..forms import FichajeForm, FichajeSocioForm
from django.urls import reverse


class GestionFichajeSocioCreateView(
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
    PermissionRequiredMixin,
    SharedFormMixin,
    CreateView,
):
    model = Fichaje
    form_class = FichajeSocioForm
    template_name = 'clubes/fichaje/gestion_fichaje_form.html'
    permission_required = 'clubes.gestionar_club'
    rol_requerido = ['CLUB_ADMIN']

    def get_socio(self):
        if not hasattr(self, '_socio'):
            self._socio = get_object_or_404(
                Socio.objects.select_related(
                    'perfil_club__perfil',
                    'perfil_club__club',
                ),
                pk=self.kwargs['socio_pk'],
                perfil_club__club_id=self.kwargs['pk'],
            )
        return self._socio

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['club'] = self.get_socio().perfil_club.club
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.socio = self.get_socio()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        socio = self.get_socio()
        club = socio.perfil_club.club
        context['socio'] = socio
        context['club'] = club
        context['titulo'] = (
            f'Fichar a {socio.perfil_club.perfil.nombre} '
            f'{socio.perfil_club.perfil.apellido}'
        )
        context['url_volver'] = 'clubes:gestionar_club'
        context['url_volver_pk'] = club.pk
        return context

    def get_success_url(self):
        return reverse_lazy(
            'clubes:gestionar_club',
            kwargs={'pk': self.kwargs['pk']},
        )


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