from pyexpat.errors import messages

from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.db.models import Q
from apps.clubes.models import Club
from django.views.generic import ListView
from django.views.generic import CreateView
from ..views.shared_views import SharedFormMixin
from ..forms import ClubForm

class ClubCreateView(SharedFormMixin, CreateView):
    model = Club
    form_class = ClubForm
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de crear un club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo club'
        context['url_volver'] = 'clubes:listar_clubes'
        return context

class ClubDetailView(ListView):
    model = Club
    template_name = 'clubes/club_detail.html'
    context_object_name = 'clubes'  # Nombre del contexto para acceder a los clubes en la plantilla

    def get_queryset(self):
        # Filtra los clubes por el ID proporcionado en la URL
        club = self.kwargs.get('club')
        return Club.objects.filter(id=club)

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

    def dispatch(self, request, *args, **kwargs):
        club_id = kwargs.get('pk')
        club = Club.objects.filter(id=club_id).first()
        if not club:
            messages.error(request, "El club no existe.")
            return redirect('clubes:listar_clubes')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        club_id = kwargs.get('pk')
        club = Club.objects.filter(id=club_id).first()
        context = {'club': club}
        return render(request, self.template_name, context)