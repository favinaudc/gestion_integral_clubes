from apps.clubes.models import AsignacionEntrenador, Club, Entrenador
from apps.customauth.mixins import (
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
)
from apps.customauth.models import Perfil, PerfilClub, Usuario
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from ..forms import EntrenadorForm, GestionCrearEntrenadorForm
from ..mixins import SharedFormMixin


class GestionCrearEntrenador(
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
    PermissionRequiredMixin,
    FormView,
):
    form_class = GestionCrearEntrenadorForm
    template_name = 'clubes/club/crear_entrenador.html'
    rol_requerido = ['CLUB_ADMIN']
    permission_required = 'clubes.gestionar_club'

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['club'] = self.get_club()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear entrenador'
        context['club'] = self.get_club()
        context['url_volver'] = 'clubes:gestionar_club'
        context['url_volver_pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse_lazy(
            'clubes:gestionar_club',
            kwargs={'pk': self.kwargs['pk']},
        )

    def form_valid(self, form):
        datos = form.cleaned_data
        club = self.get_club()

        with transaction.atomic():
            usuario = form.usuario_existente
            if usuario is None:
                usuario = Usuario.objects.create_user(
                    cuit_cuil=datos['cuit_cuil'],
                    email=datos['email'],
                    password=datos['dni'],
                )
                perfil, _ = Perfil.objects.get_or_create(usuario=usuario)
                perfil.nombre = datos['nombre']
                perfil.apellido = datos['apellido']
                perfil.dni = datos['dni']
                perfil.email = datos['email']
                perfil.fecha_nacimiento = datos['fecha_nacimiento']
                perfil.telefono = datos['telefono'] or None
                perfil.direccion = datos['direccion'] or None
                perfil.save()
            else:
                perfil, _ = Perfil.objects.get_or_create(usuario=usuario)

            entrenador, _ = Entrenador.objects.get_or_create(
                usuario=usuario,
                defaults={'experiencia': datos['experiencia']},
            )
            entrenador.club.add(club)
            grupo_entrenador, _ = Group.objects.get_or_create(
                name='ENTRENADOR'
            )
            membresia = PerfilClub.objects.filter(
                perfil=perfil,
                club=club,
                grupo_rol=grupo_entrenador,
            ).first()
            if membresia is None:
                membresia = PerfilClub.objects.create(
                    perfil=perfil,
                    club=club,
                    grupo_rol=grupo_entrenador,
                )

            for disciplina, categoria in datos['asignaciones']:
                AsignacionEntrenador.objects.get_or_create(
                    entrenador=entrenador,
                    perfil_club=membresia,
                    disciplina=disciplina,
                    categoria=categoria,
                )

        messages.success(
            self.request,
            'Entrenador y asignaciones guardados correctamente.',
        )
        return redirect(self.get_success_url())


class EntrenadorCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = Entrenador
    form_class = EntrenadorForm
    success_url = reverse_lazy(
        "clubes:listar_entrenadores"
    )  # Redirige a la lista de entrenadores después de crear un entrenador

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear entrenador"
        context["url_volver"] = (
            "clubes:listar_entrenadores"  # URL para el botón de volver
        )
        return context


class EntrenadorDetailView(LoginRequiredMixinConMensaje, DetailView):
    model = Entrenador
    template_name = "clubes/entrenador/entrenador_detail.html"
    context_object_name = "entrenador"  # Nombre del contexto para acceder a los entrenadores en la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url_volver"] = (
            "clubes:listar_entrenadores"  # URL para el botón de volver
        )
        return context


class EntrenadorListView(LoginRequiredMixinConMensaje, ListView):
    model = Entrenador
    template_name = "clubes/entrenador/entrenador_list.html"
    context_object_name = "entrenadores"  # Nombre del contexto para acceder a los entrenadores en la plantilla

    def get_queryset(self):
        entrenadores = Entrenador.objects.prefetch_related("club").all()
        return entrenadores
        # Prefetch related para optimizar consultas


class EntrenadorUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = Entrenador
    form_class = EntrenadorForm
    success_url = reverse_lazy(
        "clubes:listar_entrenadores"
    )  # Redirige a la lista de entrenadores después de editar un entrenador

    def dispatch(self, request, *args, **kwargs):
        # Aquí puedes agregar lógica adicional antes de procesar la solicitud
        if not request.user == self.get_object().usuario:
            raise PermissionDenied("No tienes permiso para editar este entrenador.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar entrenador"
        context["url_volver"] = "home"
        return context


class EntrenadorDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = Entrenador
    template_name = "clubes/entrenador_confirm_delete.html"  # Plantilla por defecto que busca Django
    success_url = reverse_lazy(
        "clubes:listar_entrenadores"
    )  # Redirige a la lista después de eliminar un entrenador
