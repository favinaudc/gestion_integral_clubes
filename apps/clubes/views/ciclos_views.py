from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.db.models import Count
from apps.clubes.models import Ciclo
from django.views.generic import ListView
from django.views.generic import CreateView
from ..mixins import SharedFormMixin
from ..forms import CicloForm

class CicloCreateView(SharedFormMixin, CreateView):
    model = Ciclo
    form_class = CicloForm  
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista de clubes después de crear un ciclo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear ciclo'
        context['url_volver'] = 'clubes:listar_ciclos'
        return context

class CicloListView(ListView):
    model = Ciclo
    template_name = 'clubes/ciclo/ciclos_list.html'
    context_object_name = 'ciclos'  # Nombre del contexto para acceder a los ciclos en la plantilla

    def get_queryset(self):
        """
        Anotamos la cantidad de clubes para evitar consultas repetitivas en el template.
        Ordenamos por año de forma descendente (el más nuevo primero).
        """
        return Ciclo.objects.annotate(
            total_clubes=Count('clubes_participantes')
        ).order_by('-año')

class CicloDetailView(DetailView):
    model = Ciclo
    template_name = ''
    context_object_name = 'ciclo'

    

class CicloUpdateView(SharedFormMixin, UpdateView):
    model = Ciclo
    form_class = CicloForm
    # template_name = 'clubes/ciclo_form.html'  # apunto a reutilizar el formulario de creacion
    success_url = reverse_lazy('clubes:listar_ciclos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar ciclo {self.object}'
        return context

class CicloDeleteView(DeleteView):
    model = Ciclo
    template_name = 'clubes/ciclo/ciclo_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista después de eliminar    
