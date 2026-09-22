from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy    
from .models import *
from .forms import CicloForm, ClubForm, SocioForm, EntrenadorForm, DisciplinaForm, CategoriaForm, FichajeForm, ParametroEvaluacionForm, PlanillaExamenForm, ResultadoExamenForm, MetricaRegistradaForm
from django_tables2 import SingleTableView
from .tables import CicloTable
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

class SharedFormMixin:
    template_name = 'templates/form.html'  # Plantilla por defecto para los formularios
    
              

class CicloCreateView(CreateView):
    model = Ciclo
    form_class = CicloForm  
    template_name = 'clubes/ciclo_form.html'
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista de clubes después de crear un ciclo

class CicloListView(ListView):
    model = Ciclo
    template_name = 'clubes/ciclo/ciclo_list.html'
    context_object_name = 'ciclos'  # Nombre del contexto para acceder a los ciclos en la plantilla
#class CicloListView(SingleTableView):
 #   model = Ciclo
  #  table_class = CicloTable
   # template_name = 'clubes/ciclo_list1.html' # Ruta a tu template
  #  context_object_name = 'ciclos'
    #(Si estás usando vistas basadas en funciones tradicionales, simplemente instancias la tabla en tu 
     #vista pasándole el queryset: table = CicloTable(Ciclo.objects.all()) y la envías en el contexto).

class CicloUpdateView(UpdateView):
    model = Ciclo
    form_class = CicloForm
    template_name = 'clubes/ciclo_form.html'  # apunto a reutilizar el formulario de creacion
    success_url = reverse_lazy('clubes:listar_ciclos')

class CicloDeleteView(DeleteView):
    model = Ciclo
    template_name = 'clubes/ciclo_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista después de eliminar    

class ClubCreateView(CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubes/club_form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de crear un club

class ClubListView(ListView):
    model = Club
    template_name = 'clubes/club_list.html'
    context_object_name = 'clubes'  # Nombre del contexto para acceder a los clubes en la plantilla  

class ClubUpdateView(UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubes/club_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de editar un club

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'clubes/club_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista después de eliminar un club

class SocioCreateView(SharedFormMixin, CreateView):
    model = Socio
    form_class = SocioForm
    template_name = 'clubes/socio/socio_form.html'
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista de socios después de crear un socio      

class SocioListView(ListView):
    model = Socio
    template_name = 'clubes/socio/socio_list.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

class SocioUpdateView(UpdateView):
    model = Socio
    form_class = SocioForm
    template_name = 'clubes/socio/socio_form.html'  # apunto a reutilizar el formulario de creacion
    success_url = reverse_lazy('clubes:socio_list')  # Redirige a la lista de socios después de editar un socio

class SocioDeleteView(DeleteView):
    model = Socio
    template_name = 'clubes/socio/socio_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:socio_list')  # Redirige a la lista después de eliminar un socio

class EntrenadorCreateView(CreateView):
    model = Entrenador
    form_class = EntrenadorForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de crear un entrenador  

class EntrenadorListView(ListView):
    model = Entrenador
    template_name = 'clubes/entrenador_list.html'
    context_object_name = 'entrenadores'  # Nombre del contexto para acceder a los entrenadores en la plantilla 

class EntrenadorUpdateView(UpdateView):
    model = Entrenador
    form_class = EntrenadorForm
    template_name = 'clubes/entrenador_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de editar un entrenador 

class EntrenadorDeleteView(DeleteView):
    model = Entrenador
    template_name = 'clubes/entrenador_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista después de eliminar un entrenador   

class DisciplinaCreateView(CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de crear una disciplina

class DisciplinaListView(ListView):
    model = Disciplina
    template_name = 'clubes/disciplina_list.html'
    context_object_name = 'disciplinas'  # Nombre del contexto para acceder a las disciplinas en la plantilla   

class DisciplinaUpdateView(UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'clubes/disciplina_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de editar una disciplina

class DisciplinaDeleteView(DeleteView):
    model = Disciplina
    template_name = 'clubes/disciplina_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista después de eliminar una disciplina

class CategoriaCreateView(CreateView):  
    model = Categoria
    form_class = CategoriaForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista de categorías después de crear una categoría

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'clubes/categoria_list.html'
    context_object_name = 'categorias'  # Nombre del contexto para acceder a las categorías en la plantilla

class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'clubes/categoria_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista de categorías después de editar una categoría

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'clubes/categoria_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista después de eliminar una categoría

class FichajeCreateView(CreateView):
    model = Fichaje
    form_class = FichajeForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de crear un fichaje

class FichajeListView(ListView):
    model = Fichaje
    template_name = 'clubes/fichaje_list.html'
    context_object_name = 'fichajes'  # Nombre del contexto para acceder a los fichajes en la plantilla

class FichajeUpdateView(UpdateView):
    model = Fichaje
    form_class = FichajeForm
    template_name = 'clubes/fichaje_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de editar un fichaje

class FichajeDeleteView(DeleteView):
    model = Fichaje
    template_name = 'clubes/fichaje_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista después de eliminar un fichaje

class PlanillaExamenCreateView(CreateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

class PlanillaExamenListView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_list.html'
    context_object_name = 'planillas'  # Nombre del contexto para acceder a las planillas de examen en la plantilla

class PlanillaExamenUpdateView(UpdateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    template_name = 'clubes/planilla_examen_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de editar una planilla

class PlanillaExamenDeleteView(DeleteView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista después de eliminar una planilla de examen

class ParametroEvaluacionCreateView(CreateView):
    model = ParametroEvaluacion
    form_class = ParametroEvaluacionForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista de parámetros de evaluación después de crear un parámetro

class ParametroEvaluacionListView(ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_list.html'
    context_object_name = 'parametros'  # Nombre del contexto para acceder a los parámetros de evaluación en la plantilla

class ParametroEvaluacionUpdateView(UpdateView):
    model = ParametroEvaluacion
    form_class = ParametroEvaluacionForm
    template_name = 'clubes/parametro_evaluacion_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista de parámetros de evaluación después de editar un parámetro

class ParametroEvaluacionDeleteView(DeleteView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista después de eliminar un parámetro de evaluación

class PlanillaExamenDetailView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_detail.html'
    context_object_name = 'planillas'  # Nombre del contexto para acceder a las planillas de examen en la plantilla

    def get_queryset(self):
        # Filtra las planillas de examen por el ID del fichaje proporcionado en la URL
        fichaje_id = self.kwargs.get('fichaje_id')
        return PlanillaExamen.objects.filter(fichaje_id=fichaje_id)

class FichajeDetailView(ListView):
    model = Fichaje
    template_name = 'clubes/fichaje_detail.html'
    context_object_name = 'fichajes'  # Nombre del contexto para acceder a los fichajes en la plantilla

    def get_queryset(self):
        # Filtra los fichajes por el ID del socio proporcionado en la URL
        socio_id = self.kwargs.get('socio_id')
        return Fichaje.objects.filter(socio_id=socio_id)

class DisciplinaDetailView(ListView):
    model = Disciplina
    template_name = 'clubes/disciplina_detail.html'
    context_object_name = 'disciplinas'  # Nombre del contexto para acceder a las disciplinas en la plantilla

    def get_queryset(self):
        # Filtra las disciplinas por el ID del club proporcionado en la URL
        club_id = self.kwargs.get('club_id')
        return Disciplina.objects.filter(club_id=club_id)

class CategoriaDetailView(ListView):
    model = Categoria
    template_name = 'clubes/categoria_detail.html'
    context_object_name = 'categorias'  # Nombre del contexto para acceder a las categorías en la plantilla

    def get_queryset(self):
        # Filtra las categorías por el ID de la disciplina proporcionado en la URL
        disciplina_id = self.kwargs.get('disciplina_id')
        return Categoria.objects.filter(disciplina_id=disciplina_id)

class EntrenadorDetailView(ListView):
    model = Entrenador
    template_name = 'clubes/entrenador_detail.html'
    context_object_name = 'entrenadores'  # Nombre del contexto para acceder a los entrenadores en la plantilla

    def get_queryset(self):
        # Filtra los entrenadores por el ID del club proporcionado en la URL
        club_id = self.kwargs.get('club_id')
        return Entrenador.objects.filter(club_id=club_id)

class SocioDetailView(ListView):
    model = Socio
    template_name = 'clubes/socio_detail.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

    def get_queryset(self):
        # Filtra los socios por el ID del club proporcionado en la URL
        club_id = self.kwargs.get('club_id')
        return Socio.objects.filter(club_id=club_id)

class ClubDetailView(ListView):
    model = Club
    template_name = 'clubes/club_detail.html'
    context_object_name = 'clubes'  # Nombre del contexto para acceder a los clubes en la plantilla

    def get_queryset(self):
        # Filtra los clubes por el ID proporcionado en la URL
        club_id = self.kwargs.get('club_id')
        return Club.objects.filter(id=club_id)

class ParametroEvaluacionDetailView(ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_detail.html'
    context_object_name = 'parametros'  # Nombre del contexto para acceder a los parámetros de evaluación en la plantilla

    def get_queryset(self):
        # Filtra los parámetros de evaluación por el ID proporcionado en la URL
        parametro_id = self.kwargs.get('parametro_id')
        return ParametroEvaluacion.objects.filter(id=parametro_id)

class ResultadoExamenCreateView(CreateView):
    model = PlanillaExamen
    form_class = ResultadoExamenForm
    template_name = 'clubes/resultado_examen_form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

class ResultadoExamenListView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_list.html'
    context_object_name = 'resultados'  # Nombre del contexto para acceder a los resultados de examen en la plantilla

class ResultadoExamenUpdateView(UpdateView):
    model = PlanillaExamen
    form_class = ResultadoExamenForm
    template_name = 'clubes/resultado_examen_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_resultados_examen')  # Redirige a la lista de resultados de examen después de editar un resultado

class ResultadoExamenDeleteView(DeleteView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_confirm_delete.html'
    success_url = reverse_lazy('clubes:listar_resultados_examen')

class ResultadoExamenDetailView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_detail.html'
    context_object_name = 'resultados'  # Nombre del contexto para acceder a los resultados de examen en la plantilla

    def get_queryset(self):
        # Filtra los resultados de examen por el ID del fichaje proporcionado en la URL
        fichaje_id = self.kwargs.get('fichaje_id')
        return PlanillaExamen.objects.filter(fichaje_id=fichaje_id)

class MetricaRegistradaCreateView(CreateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    template_name = 'clubes/metrica_registrada_form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de crear una métrica

class MetricaRegistradaListView(ListView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica_registrada_list.html'
    context_object_name = 'metricas'  # Nombre del contexto para acceder a las métricas registradas en la plantilla

class MetricaRegistradaUpdateView(UpdateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    template_name = 'clubes/metrica_registrada_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de editar una métrica

class MetricaRegistradaDeleteView(DeleteView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica_registrada_confirm_delete.html'
    success_url = reverse_lazy('clubes:listar_metricas_registradas')
