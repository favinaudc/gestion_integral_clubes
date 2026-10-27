from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.db.models import Q
from apps.clubes.models import Disciplina, Club
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from apps.customauth.mixins import LoginRequiredMixinConMensaje
from ..mixins import SharedFormMixin
from ..forms import DisciplinaForm
from django.shortcuts import get_object_or_404

class DisciplinaCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de crear una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Crear disciplina'
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
        context['titulo'] = f'Editar disciplina'
        context['url_volver'] = 'clubes:listar_disciplinas'
        return context

class DisciplinaDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = Disciplina
    template_name = 'clubes/disciplina_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista después de eliminar una disciplina