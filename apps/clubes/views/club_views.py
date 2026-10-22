from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.db.models import Q
from apps.clubes.models import Club
from django.views.generic import ListView
from django.views.generic import CreateView
from ..views.shared_views import SharedFormMixin
from ..forms import ClubForm

class ClubCreateView(SharedFormMixin, CreateView):
    model = Club
    form_class = ClubForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo club'
        context['url_volver'] = 'clubes:listar_clubes'
        return context

    def get_success_url(self): #pone el pk en la url .
        print("self.object.pk", self.object.pk)
        return reverse_lazy('clubes:detalles_club', kwargs={'pk': self.object.pk})

class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubes/club/club_detail.html'
    context_object_name = 'club'  # Nombre del contexto para acceder al club en la plantilla

    

class ClubListView(ListView):
    model = Club
    template_name = 'clubes/club/club_list.html'
    context_object_name = 'clubes'  # Nombre del contexto para acceder a los clubes en la plantilla  

    def get_queryset(self):
        queryset = super().get_queryset()
        
        q = self.request.GET.get('q')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')

        # Filtro de texto (búsqueda en múltiples campos con OR)
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(direccion__icontains=q) |
                Q(email__icontains=q)
            )
        
        # Filtros de fecha de fundación (Rango)
        if fecha_desde:
            queryset = queryset.filter(fecha_fundacion__gte=fecha_desde)
            
        if fecha_hasta:
            queryset = queryset.filter(fecha_fundacion__lte=fecha_hasta)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context

class ClubUpdateView(SharedFormMixin, UpdateView):
    model = Club
    form_class = ClubForm
    # template_name = 'clubes/club_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de editar un club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar club {self.object}'
        context['url_volver'] = 'clubes:listar_clubes'
        return context

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'clubes/club_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista después de eliminar un club


class GestionarClubView(View):
    template_name = 'clubes/club/club_gestion.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)