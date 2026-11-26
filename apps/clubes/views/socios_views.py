from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from apps.customauth.mixins import LoginRequiredMixinConMensaje, ValidarRolClubMixin
from apps.customauth.models import Perfil, PerfilClub
from django.urls import reverse_lazy
from apps.clubes.models import Club, Socio
from ..mixins import SharedFormMixin
from ..forms import SocioForm


class SocioMembershipSaveMixin:
    def form_valid(self, form):
        previous_membership = None
        if self.object and self.object.pk:
            previous_membership = self.object.perfil_club

        with transaction.atomic():
            socio = form.save(commit=False)
            usuario = form.cleaned_data.get('usuario')
            if usuario is None and previous_membership:
                usuario = previous_membership.perfil.usuario

            if usuario:
                perfil, _ = Perfil.objects.get_or_create(usuario=usuario)
            elif previous_membership:
                perfil = previous_membership.perfil
            else:
                perfil = Perfil()

            perfil.nombre = form.cleaned_data['nombre']
            perfil.apellido = form.cleaned_data['apellido']
            perfil.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            perfil.telefono = form.cleaned_data['telefono']
            perfil.direccion = form.cleaned_data['direccion']
            perfil.save()

            club = form.cleaned_data['club']
            grupo_socio, _ = Group.objects.get_or_create(name='SOCIO')
            membership, _ = PerfilClub.objects.get_or_create(
                perfil=perfil,
                club=club,
                grupo_rol=grupo_socio,
            )

            socio.perfil_club = membership
            socio.save()

            if usuario:
                usuario.groups.add(grupo_socio)

            if previous_membership and previous_membership.pk != membership.pk:
                previous_membership.delete()

            self.object = socio

        return redirect(self.get_success_url())


class GestionSocioMixin(
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
    PermissionRequiredMixin,
):
    model = Socio
    rol_requerido = ['CLUB_ADMIN']
    permission_required = 'clubes.gestionar_club'
    pk_url_kwarg = 'socio_pk'

    def get_queryset(self):
        return Socio.objects.filter(
            perfil_club__club_id=self.kwargs['pk'],
        ).select_related(
            'perfil_club__perfil',
            'perfil_club__perfil__usuario',
            'perfil_club__club',
            'tutor_responsable__perfil_club__perfil',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.object.perfil_club.club
        context['titulo'] = self.titulo
        context['url_volver'] = 'clubes:gestionar_club'
        context['url_volver_pk'] = self.object.perfil_club.club_id
        return context


class GestionSocioDetailView(GestionSocioMixin, DetailView):
    context_object_name = 'socio'
    template_name = 'clubes/socio/gestion_socio_detalle.html'
    titulo = 'Detalle del socio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fichajes'] = self.object.fichajes.select_related(
            'disciplina',
            'categoria',
        ).order_by('-fecha_fichaje', '-pk')
        return context


class GestionSocioUpdateView(
    GestionSocioMixin,
    SharedFormMixin,
    SocioMembershipSaveMixin,
    UpdateView,
):
    form_class = SocioForm
    template_name = 'clubes/form_template.html'
    titulo = 'Editar socio'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['require_tutor_for_minor'] = False
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        club = self.object.perfil_club.club
        form.fields['club'].queryset = Club.objects.filter(pk=club.pk)
        form.fields['club'].initial = club.pk
        form.fields['club'].disabled = True
        form.fields['tutor_responsable'].queryset = Socio.objects.filter(
            perfil_club__club_id=club.pk,
            es_tutor=True,
        ).exclude(pk=self.object.pk)
        form.helper.form_tag = False
        return form

    def get_success_url(self):
        return reverse_lazy(
            'clubes:gestionar_club',
            kwargs={'pk': self.object.perfil_club.club_id},
        )


class SocioCreateView(
    LoginRequiredMixinConMensaje,
    SharedFormMixin,
    SocioMembershipSaveMixin,
    CreateView,
):
    model = Socio
    form_class = SocioForm
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista de socios después de crear un socio      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear socio'
        context['url_volver'] = 'clubes:listar_socios'  # URL para el botón de volver
        return context


class SocioDetailView(LoginRequiredMixinConMensaje, ListView):
    model = Socio
    template_name = 'clubes/socio_detail.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

    def get_queryset(self):
        # Filtra los socios por el ID del club proporcionado en la URL
        club = self.kwargs.get('club')
        return Socio.objects.filter(perfil_club__club=club).select_related(
            'perfil_club__perfil',
            'perfil_club__club',
        )

class SocioListView(LoginRequiredMixinConMensaje, ListView):
    model = Socio
    template_name = 'clubes/socio/socio_list.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

    def get_queryset(self):
        return super().get_queryset().select_related(
            'perfil_club__perfil',
            'perfil_club__club',
        )


class SocioUpdateView(
    LoginRequiredMixinConMensaje,
    SharedFormMixin,
    SocioMembershipSaveMixin,
    UpdateView,
):
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

    def form_valid(self, form):
        membership = self.object.perfil_club
        response = super().form_valid(form)
        membership.delete()
        return response