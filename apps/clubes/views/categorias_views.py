from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from apps.clubes.models import Categoria
from django.views.generic import ListView
from django.views.generic import CreateView
from apps.clubes.views import SharedFormMixin


class CategoriaCreateView(SharedFormMixin,CreateView):  
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista de categorías después de crear una categoría

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['titulo'] =f'Crear categoria'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Envuelve el objeto en una lista [ ] para que sea iterable
        club = form.cleaned_data.get('club')
        if club:
            # Si es un solo objeto, ponlo entre corchetes
            self.object.club.set([club]) 
            
        return response

class CategoriaDetailView(ListView):
    model = Categoria
    template_name = 'clubes/categoria_detail.html'
    context_object_name = 'categorias'  # Nombre del contexto para acceder a las categorías en la plantilla

    def get_queryset(self):
        # Filtra las categorías por el ID de la disciplina proporcionado en la URL
        disciplina = self.kwargs.get('disciplina')
        return Categoria.objects.filter(disciplina=disciplina)


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'clubes/categoria/categoria_list.html'
    context_object_name = 'categorias'  # Nombre del contexto para acceder a las categorías en la plantilla

class CategoriaUpdateView(SharedFormMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista de categorías después de editar una categoría

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Editar categoria {self.object}'
        return context

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'clubes/categoria_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista después de eliminar una categoría