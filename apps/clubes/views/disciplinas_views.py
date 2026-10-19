from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.db.models import Q
from apps.clubes.models import Disciplina
from django.views.generic import ListView
from django.views.generic import CreateView
from apps.clubes.views import SharedFormMixin


class DisciplinaCreateView(SharedFormMixin, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de crear una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Crear disciplina'
        context['url_volver'] = 'clubes:listar_disciplinas'
        return context

class DisciplinaDetailView(ListView):
    model = Disciplina
    template_name = 'clubes/disciplina_detail.html'
    context_object_name = 'disciplinas'  # Nombre del contexto para acceder a las disciplinas en la plantilla

    def get_queryset(self):
        # Filtra las disciplinas por el ID del club proporcionado en la URL
        club = self.kwargs.get('club')
        return Disciplina.objects.filter(club=club)


class DisciplinaListView(ListView):
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

class DisciplinaUpdateView(SharedFormMixin, UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de editar una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar disciplina'
        return context

class DisciplinaDeleteView(DeleteView):
    model = Disciplina
    template_name = 'clubes/disciplina_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista después de eliminar una disciplina