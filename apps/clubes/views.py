from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy    
from .models import *
from .forms import CicloForm


# Create your views here.

CLUBES_DB = {
    1: {
        'nombre': 'Club Social y Deportivo Rawson',
        'disciplinas': [
            {
                'nombre': 'Rugby',
                'categorias': ['M6', 'M8', 'M14', 'M16', 'Primera']
            },
            {
                'nombre': 'Hockey',
                'categorias': ['Infantiles', 'Sub-14', 'Sub-16', 'Primera']
            }
        ]
    },
    2: {
        'nombre': 'Club Atlético Trelew',
        'disciplinas': [
            {
                'nombre': 'Fútbol',
                'categorias': ['Escuelita', 'Novena', 'Séptima', 'Primera']
            },
            {
                'nombre': 'Básquet',
                'categorias': ['Mini', 'U13', 'U15', 'U17', 'Primera']
            }
        ]
    },
    3: {
        'nombre': 'Puerto Madryn Rugby Club',
        'disciplinas': [
            {
                'nombre': 'Rugby',
                'categorias': ['M10', 'M12', 'M16', 'M18', 'Plantel Superior']
            }
        ]
    }
}

def clubes(request):
    lista_clubes = []
    
    for club_id, datos in CLUBES_DB.items():
        total_disciplinas = len(datos['disciplinas'])
        # Sumamos la cantidad de categorías de cada disciplina
        total_categorias = sum(len(d['categorias']) for d in datos['disciplinas'])
        
        lista_clubes.append({
            'id': club_id,
            'nombre': datos['nombre'],
            'total_disciplinas': total_disciplinas,
            'total_categorias': total_categorias,
        })

    context = {
        'clubes': lista_clubes,
    }

    return render(request, 'clubes/clubes.html', context)

def categorias(request, club_id):

    club = CLUBES_DB.get(club_id) 
    
    if not club:
        raise Http404(f"No se encontró información para el club con ID {club_id}")

    context = {
        'club_id': club_id,
        'nombre_club': club['nombre'],
        'disciplinas': club['disciplinas'],
    }

    return render(request, 'clubes/categorias.html', context)

class CicloCreateView(CreateView):
    model = Ciclo
    form_class = CicloForm  
    template_name = 'clubes/ciclo_form.html'
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista de clubes después de crear un ciclo

class CicloListView(ListView):
    model = Ciclo
    template_name = 'clubes/ciclo_list.html'
    context_object_name = 'ciclos'  # Nombre del contexto para acceder a los ciclos en la plantilla
