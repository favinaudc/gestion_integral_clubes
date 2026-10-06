from django.template import context
from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy    
from .models import *
from .forms import CicloForm, ClubForm, SocioForm, EntrenadorForm, DisciplinaForm, CategoriaForm, FichajeForm, ParametroEvaluacionForm, PlanillaExamenForm, ResultadoExamenForm, MetricaRegistradaForm
from django_tables2 import SingleTableView
from .tables import CicloTable
# Create your views here.

class SharedFormMixin:
    template_name = 'clubes/form_template.html'  # Plantilla por defecto para los formularios

class CicloCreateView(SharedFormMixin, CreateView):
    model = Ciclo
    form_class = CicloForm  
    # template_name = 'clubes/ciclo_form.html'
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista de clubes después de crear un ciclo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear ciclo'
        return context

class CicloListView(ListView):
    model = Ciclo
    template_name = 'clubes/ciclo/ciclos_list.html'
    context_object_name = 'ciclos'  # Nombre del contexto para acceder a los ciclos en la plantilla


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
    template_name = 'clubes/ciclo_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_ciclos')  # Redirige a la lista después de eliminar    

class ClubCreateView(SharedFormMixin, CreateView):
    model = Club
    form_class = ClubForm
    # template_name = 'clubes/club_form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de crear un club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo club'
        return context

class ClubListView(ListView):
    model = Club
    template_name = 'clubes/club/club_list.html'
    context_object_name = 'clubes'  # Nombre del contexto para acceder a los clubes en la plantilla  

class ClubUpdateView(SharedFormMixin, UpdateView):
    model = Club
    form_class = ClubForm
    # template_name = 'clubes/club_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de editar un club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar club {self.object}'
        return context

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'clubes/club_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista después de eliminar un club

class SocioCreateView(SharedFormMixin, CreateView):
    model = Socio
    form_class = SocioForm
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista de socios después de crear un socio      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear socio{self.object}'
        return context
    
class SocioListView(ListView):
    model = Socio
    template_name = 'clubes/socio/socio_list.html'
    context_object_name = 'socios'  # Nombre del contexto para acceder a los socios en la plantilla

class SocioUpdateView(SharedFormMixin, UpdateView):
    model = Socio
    form_class = SocioForm
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista de socios después de editar un socio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = f'Editar socio{self.object}'
        return context

class SocioDeleteView(DeleteView):
    model = Socio
    template_name = 'clubes/socio/socio_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_socios')  # Redirige a la lista después de eliminar un socio

class EntrenadorCreateView(SharedFormMixin, CreateView):
    model = Entrenador
    form_class = EntrenadorForm
    template_name = 'clubes/form.html'  # Plantilla para el formulario de creación
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de crear un entrenador  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear entrenador{self.object}'
        return context

class EntrenadorListView(ListView):
    model = Entrenador
    template_name = 'clubes/entrenador_list.html'
    context_object_name = 'entrenadores'  # Nombre del contexto para acceder a los entrenadores en la plantilla 

class EntrenadorUpdateView(SharedFormMixin, UpdateView):
    model = Entrenador
    form_class = EntrenadorForm
    template_name = 'clubes/entrenador_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista de entrenadores después de editar un entrenador 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']= f'Editar entrenador{self.object}'
        return context

class EntrenadorDeleteView(DeleteView):
    model = Entrenador
    template_name = 'clubes/entrenador_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_entrenadores')  # Redirige a la lista después de eliminar un entrenador   

class DisciplinaCreateView(SharedFormMixin, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de crear una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Crear disciplina{self.object}'
        return context

class DisciplinaListView(ListView):
    model = Disciplina
    template_name = 'clubes/disciplina_list.html'
    context_object_name = 'disciplinas'  # Nombre del contexto para acceder a las disciplinas en la plantilla   

class DisciplinaUpdateView(SharedFormMixin, UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista de disciplinas después de editar una disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar disciplina{self.object}'
        return context

class DisciplinaDeleteView(DeleteView):
    model = Disciplina
    template_name = 'clubes/disciplina_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_disciplinas')  # Redirige a la lista después de eliminar una disciplina

class CategoriaCreateView(SharedFormMixin,CreateView):  
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista de categorías después de crear una categoría

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['titulo'] =f'Crear categoria{self.object}'
        return context

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'clubes/categoria_list.html'
    context_object_name = 'categorias'  # Nombre del contexto para acceder a las categorías en la plantilla

class CategoriaUpdateView(SharedFormMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista de categorías después de editar una categoría

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Editar categoria{self.object}'
        return context

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'clubes/categoria_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_categorias')  # Redirige a la lista después de eliminar una categoría

class FichajeCreateView(SharedFormMixin, CreateView):
    model = Fichaje
    form_class = FichajeForm
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de crear un fichaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear fichaje{self.object}'
        return context

class FichajeListView(ListView):
    model = Fichaje
    template_name = 'clubes/fichaje_list.html'
    context_object_name = 'fichajes'  # Nombre del contexto para acceder a los fichajes en la plantilla

class FichajeUpdateView(SharedFormMixin, UpdateView):
    model = Fichaje
    form_class = FichajeForm
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista de fichajes después de editar un fichaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar fichaje{self.object}'
        return context

class FichajeDeleteView(DeleteView):
    model = Fichaje
    template_name = 'clubes/fichaje_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_fichajes')  # Redirige a la lista después de eliminar un fichaje

class PlanillaExamenCreateView(SharedFormMixin, CreateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear planilla de examen{self.object}'
        return context

class PlanillaExamenListView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_list.html'
    context_object_name = 'planillas'  # Nombre del contexto para acceder a las planillas de examen en la plantilla

class PlanillaExamenUpdateView(SharedFormMixin, UpdateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de editar una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar planilla de examen{self.object}'
        return context

class PlanillaExamenDeleteView(DeleteView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista después de eliminar una planilla de examen

class ParametroEvaluacionCreateView(SharedFormMixin, CreateView):
    model = ParametroEvaluacion
    form_class = ParametroEvaluacionForm
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista de parámetros de evaluación después de crear un parámetro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Crear parametro de elvaluacion{self.object}'
        return context
    
class ParametroEvaluacionListView(ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_list.html'
    context_object_name = 'parametros'  # Nombre del contexto para acceder a los parámetros de evaluación en la plantilla

class ParametroEvaluacionUpdateView(SharedFormMixin, UpdateView):
    model = ParametroEvaluacion
    form_class = ParametroEvaluacionForm
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista de parámetros de evaluación después de editar un parámetro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar parámetro de evaluación {self.object}'
        return context

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

class ResultadoExamenCreateView(SharedFormMixin, CreateView):
    model = PlanillaExamen
    form_class = ResultadoExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear resultado de examen{self.object}'
        return context
    
class ResultadoExamenListView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_list.html'
    context_object_name = 'resultados'  # Nombre del contexto para acceder a los resultados de examen en la plantilla

class ResultadoExamenUpdateView(SharedFormMixin, UpdateView):
    model = PlanillaExamen
    form_class = ResultadoExamenForm
    success_url = reverse_lazy('clubes:listar_resultados_examen')  # Redirige a la lista de resultados de examen después de editar un resultado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar resultado de examen {self.object}'
        return context

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

class MetricaRegistradaCreateView(SharedFormMixin, CreateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de crear una métrica

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear métrica registrada{self.object}'
        return context
    
class MetricaRegistradaListView(ListView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica_registrada_list.html'
    context_object_name = 'metricas'  # Nombre del contexto para acceder a las métricas registradas en la plantilla

class MetricaRegistradaUpdateView(SharedFormMixin, UpdateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de editar una métrica

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar métrica registrada {self.object}'
        return context

class MetricaRegistradaDeleteView(DeleteView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica_registrada_confirm_delete.html'
    success_url = reverse_lazy('clubes:listar_metricas_registradas')
