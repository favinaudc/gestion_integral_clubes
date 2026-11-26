from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.clubes.models import Categoria, Club, Disciplina
from apps.customauth.mixins import (
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
)
from ..forms import (
    CategoriaForm,
    GestionCategoriaForm,
    ReutilizarCategoriaForm,
)
from ..mixins import SharedFormMixin


class GestionCategorias(
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
    PermissionRequiredMixin,
    View,
):
    rol_requerido = ['CLUB_ADMIN']
    permission_required = 'clubes.gestionar_club'
    template_name = 'clubes/club/club_categorias.html'

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs['pk'])

    def get_disciplina(self, club, disciplina_id):
        if not disciplina_id:
            return None
        return get_object_or_404(
            Disciplina,
            pk=disciplina_id,
            clubes_suscritos=club,
        )

    def get_disciplinas(self, club):
        categorias_del_club = Categoria.objects.filter(club=club).order_by(
            'nombre'
        )
        return (
            club.disciplinas.all()
            .order_by('nombre')
            .prefetch_related(
                Prefetch(
                    'categorias',
                    queryset=categorias_del_club,
                    to_attr='categorias_del_club',
                )
            )
        )

    def render_page(
        self,
        request,
        club,
        disciplina_seleccionada=None,
        form_categoria=None,
        form_reutilizar=None,
    ):
        if disciplina_seleccionada:
            if form_categoria is None:
                form_categoria = GestionCategoriaForm()
            if form_reutilizar is None:
                form_reutilizar = ReutilizarCategoriaForm(
                    club=club,
                    disciplina=disciplina_seleccionada,
                )
            categorias_asignadas = Categoria.objects.filter(
                club=club,
                disciplina=disciplina_seleccionada,
            ).order_by('nombre')
        else:
            categorias_asignadas = Categoria.objects.none()

        context = {
            'club': club,
            'disciplinas': self.get_disciplinas(club),
            'disciplina_seleccionada': disciplina_seleccionada,
            'categorias_asignadas': categorias_asignadas,
            'form_categoria': form_categoria,
            'form_reutilizar': form_reutilizar,
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        club = self.get_club()
        disciplina = self.get_disciplina(
            club,
            request.GET.get('disciplina_id'),
        )
        return self.render_page(request, club, disciplina)

    def post(self, request, *args, **kwargs):
        club = self.get_club()
        disciplina = self.get_disciplina(
            club,
            request.POST.get('disciplina_id'),
        )
        if disciplina is None:
            messages.error(request, 'Seleccioná una disciplina del club.')
            return redirect('clubes:gestion_categorias', pk=club.pk)

        accion = request.POST.get('accion')
        if accion == 'crear':
            form = GestionCategoriaForm(request.POST)
            if not form.is_valid():
                return self.render_page(
                    request,
                    club,
                    disciplina,
                    form_categoria=form,
                )

            categoria = form.save(commit=False)
            categoria.club = club
            categoria.save()
            categoria.disciplina.add(disciplina)
            messages.success(
                request,
                f'La categoría {categoria.nombre} se creó para {disciplina.nombre}.',
            )
        elif accion == 'reutilizar':
            form = ReutilizarCategoriaForm(
                request.POST,
                club=club,
                disciplina=disciplina,
            )
            if not form.is_valid():
                return self.render_page(
                    request,
                    club,
                    disciplina,
                    form_reutilizar=form,
                )

            categoria = form.cleaned_data['categoria']
            categoria.disciplina.add(disciplina)
            messages.success(
                request,
                f'La categoría {categoria.nombre} se agregó a {disciplina.nombre}.',
            )
        elif accion == 'quitar':
            categoria = get_object_or_404(
                Categoria,
                pk=request.POST.get('categoria_id'),
                club=club,
                disciplina=disciplina,
            )
            categoria.disciplina.remove(disciplina)
            messages.success(
                request,
                f'La categoría {categoria.nombre} se quitó de {disciplina.nombre}.',
            )
        else:
            messages.error(request, 'La acción solicitada no es válida.')
            return self.redirect_to_discipline(club, disciplina)

        return self.redirect_to_discipline(club, disciplina)

    def redirect_to_discipline(self, club, disciplina):
        url = reverse('clubes:gestion_categorias', kwargs={'pk': club.pk})
        return redirect(f'{url}?disciplina_id={disciplina.pk}#gestion-categoria')


class CategoriaCreateView(
    LoginRequiredMixinConMensaje,
    PermissionRequiredMixin,
    SharedFormMixin,
    CreateView,
):
    model = Categoria
    form_class = CategoriaForm
    permission_required = 'clubes.add_categoria'
    success_url = reverse_lazy('clubes:listar_categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear categoría'
        return context


class CategoriaDetailView(
    LoginRequiredMixinConMensaje,
    PermissionRequiredMixin,
    ListView,
):
    model = Categoria
    template_name = 'clubes/categoria_detail.html'
    context_object_name = 'categorias'
    permission_required = 'clubes.view_categoria'

    def get_queryset(self):
        disciplina = self.kwargs.get('disciplina')
        return Categoria.objects.filter(disciplina=disciplina)


class CategoriaListView(
    LoginRequiredMixinConMensaje,
    PermissionRequiredMixin,
    ListView,
):
    model = Categoria
    template_name = 'clubes/categoria/categoria_list.html'
    context_object_name = 'categorias'
    permission_required = 'clubes.view_categoria'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('club')
            .prefetch_related('disciplina')
            .order_by('nombre')
        )


class CategoriaUpdateView(
    LoginRequiredMixinConMensaje,
    PermissionRequiredMixin,
    SharedFormMixin,
    UpdateView,
):
    model = Categoria
    form_class = CategoriaForm
    permission_required = 'clubes.change_categoria'
    success_url = reverse_lazy('clubes:listar_categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar categoría {self.object}'
        return context


class CategoriaDeleteView(
    LoginRequiredMixinConMensaje,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Categoria
    template_name = 'clubes/categoria_confirm_delete.html'
    permission_required = 'clubes.delete_categoria'
    success_url = reverse_lazy('clubes:listar_categorias')
