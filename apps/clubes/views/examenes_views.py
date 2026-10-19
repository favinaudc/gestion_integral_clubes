from django.views.generic import DetailView
from apps.clubes.models import MetricaRegistrada
from django.views.generic import CreateView
from django.views.generic import UpdateView
from apps.clubes.views import SharedFormMixin
from django.urls import reverse_lazy
from apps.clubes.models import ParametroEvaluacion
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.clubes.models import PlanillaExamen


class PlanillaExamenCreateView(SharedFormMixin, CreateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear planilla de examen'
        return context

class PlanillaExamenListView(ListView):
    model = PlanillaExamen
    template_name = 'clubes/planillaexamen/planilla_examen_list.html'
    context_object_name = 'planillas'  # Nombre del contexto para acceder a las planillas de examen en la plantilla

class PlanillaExamenUpdateView(SharedFormMixin, UpdateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de editar una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar planilla de examen {self.object}'
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

class ParametroEvaluacionDetailView(ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_detail.html'
    context_object_name = 'parametros'  # Nombre del contexto para acceder a los parámetros de evaluación en la plantilla

    def get_queryset(self):
        # Filtra los parámetros de evaluación por el ID proporcionado en la URL
        parametro = self.kwargs.get('parametro')
        return ParametroEvaluacion.objects.filter(id=parametro)
    
class ParametroEvaluacionListView(ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/paramevalua/parametro_evaluacion_list.html'
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
        fichaje = self.kwargs.get('fichaje')
        return PlanillaExamen.objects.filter(fichaje=fichaje)

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
        fichaje = self.kwargs.get('fichaje')
        return PlanillaExamen.objects.filter(fichaje=fichaje)


class MetricaRegistradaCreateView(SharedFormMixin, CreateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de crear una métrica

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear métrica registrada{self.object}'
        return context

class MetricaRegistradaDeatilView(DetailView):
    pass
    
class MetricaRegistradaListView(ListView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica/metrica_registrada_list.html'
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