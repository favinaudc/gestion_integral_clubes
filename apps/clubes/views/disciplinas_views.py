from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.clubes.models import Club, Disciplina
from apps.customauth.mixins import (
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
)
from ..forms import DisciplinaForm
from ..mixins import SharedFormMixin


class GestionDisciplinas(
    LoginRequiredMixinConMensaje,
    ValidarRolClubMixin,
    PermissionRequiredMixin,
    View,
):
    rol_requerido = ['CLUB_ADMIN']
    permission_required = 'clubes.suscribir_club_a_disciplina'
    template_name = 'clubes/club/club_disciplinas.html'

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        club = self.get_club()
        filtro = request.GET.get('filtro', 'todas')
        disciplinas = Disciplina.objects.all()

        if filtro == 'suscriptas':
            disciplinas = club.disciplinas.all()
        elif filtro == 'no_suscriptas':
            disciplinas = disciplinas.exclude(
                pk__in=club.disciplinas.values('pk')
            )
        elif filtro != 'todas':
            filtro = 'todas'

        context = {
            'club': club,
            'disciplinas': disciplinas.order_by('nombre'),
            'disciplinas_suscriptas': set(
                club.disciplinas.values_list('pk', flat=True)
            ),
            'filtro': filtro,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        club = self.get_club()
        accion = request.POST.get('accion')
        if accion not in {'suscribir', 'desuscribir'}:
            messages.error(request, 'La acción solicitada no es válida.')
            return redirect('clubes:gestion_disciplinas', pk=club.pk)

        disciplina = get_object_or_404(
            Disciplina,
            pk=request.POST.get('disciplina_id'),
        )
        if accion == 'suscribir':
            ya_suscripta = club.disciplinas.filter(pk=disciplina.pk).exists()
            if ya_suscripta:
                messages.info(
                    request,
                    f'El club ya está suscripto a {disciplina.nombre}.',
                )
                return redirect('clubes:gestion_disciplinas', pk=club.pk)

            club.disciplinas.add(disciplina)
            messages.success(
                request,
                f'{disciplina.nombre} se agregó a las disciplinas del club.',
            )
        else:
            ya_suscripta = club.disciplinas.filter(pk=disciplina.pk).exists()
            if not ya_suscripta:
                messages.info(
                    request,
                    f'El club no estaba suscripto a {disciplina.nombre}.',
                )
                return redirect('clubes:gestion_disciplinas', pk=club.pk)

            club.disciplinas.remove(disciplina)
            messages.success(
                request,
                f'{disciplina.nombre} se quitó de las disciplinas del club.',
            )

        return redirect('clubes:gestion_disciplinas', pk=club.pk)


class DisciplinaCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de crear una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] ='Crear disciplina'
        context['url_volver'] = 'clubes:listar_disciplinas'
        return context
    def get_success_url(self): #pone el pk en la url .
            print("self.object.pk", self.object.pk)
            return reverse_lazy('clubes:detalles_disciplina', kwargs={'pk': self.object.pk})

class DisciplinaDetailView(LoginRequiredMixinConMensaje, DetailView):
    model = Disciplina
    template_name = 'clubes/disciplina/disciplina_detail.html'
    context_object_name = 'disciplina'  # Nombre del contexto para acceder a la disciplina en la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_volver'] = 'clubes:listar_disciplinas'  # URL para el botón de volver
        return context

class DisciplinaListView(LoginRequiredMixinConMensaje, ListView):
    model = Disciplina
    template_name = 'clubes/disciplina/disciplina_list.html'
    context_object_name = 'disciplinas'

    def get_queryset(self):
        """
        Sustituye la consulta global Disciplina.objects.all() por una consulta filtrada.
        """
        queryset = super().get_queryset()
        
        # Capturar el valor del input de búsqueda (name="q")
        q = self.request.GET.get('q')
        
        if q:
            # Se utilizan objetos Q para construir la lógica OR en la base de datos
            queryset = queryset.filter(
                Q(nombre__icontains=q) | 
                Q(descripcion__icontains=q)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Inyecta variables adicionales en el diccionario de contexto.
        """
        context = super().get_context_data(**kwargs)
        
        # Pasar 'q' de vuelta al template para mantener el texto escrito en el input
        context['q'] = self.request.GET.get('q', '')
        
        return context  

class DisciplinaUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de editar una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar disciplina'
        context['url_volver'] = 'clubes:listar_disciplinas'
        return context

class DisciplinaDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = Disciplina
    template_name = 'clubes/disciplina_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista después de eliminar una disciplina