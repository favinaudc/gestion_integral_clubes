from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from apps.clubes.models import MetricaRegistrada, PlanillaExamen, ParametroEvaluacion
from apps.customauth.mixins import LoginRequiredMixinConMensaje
from ..mixins import SharedFormMixin
from ..forms import PlanillaExamenForm, ParametroEvaluacionForm, ResultadoExamenForm, MetricaRegistradaForm

class PlanillaExamenCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear planilla de examen'
        return context

class PlanillaExamenListView(LoginRequiredMixinConMensaje, ListView):
    model = PlanillaExamen
    template_name = 'clubes/planillaexamen/planilla_examen_list.html'
    context_object_name = 'planillas'  # Nombre del contexto para acceder a las planillas de examen en la plantilla

class PlanillaExamenUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = PlanillaExamen
    form_class = PlanillaExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de editar una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar planilla de examen {self.object}'
        return context

class PlanillaExamenDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista después de eliminar una planilla de examen

class ParametroEvaluacionCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = ParametroEvaluacion
    form_class = ParametroEvaluacionForm
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista de parámetros de evaluación después de crear un parámetro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] =f'Crear parametro de elvaluacion{self.object}'
        return context

class ParametroEvaluacionDetailView(LoginRequiredMixinConMensaje, ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_detail.html'
    context_object_name = 'parametros'  # Nombre del contexto para acceder a los parámetros de evaluación en la plantilla

    def get_queryset(self):
        # Filtra los parámetros de evaluación por el ID proporcionado en la URL
        parametro = self.kwargs.get('parametro')
        return ParametroEvaluacion.objects.filter(id=parametro)
    
class ParametroEvaluacionListView(LoginRequiredMixinConMensaje, ListView):
    model = ParametroEvaluacion
    template_name = 'clubes/paramevalua/parametro_evaluacion_list.html'
    context_object_name = 'parametros'  # Nombre del contexto para acceder a los parámetros de evaluación en la plantilla

class ParametroEvaluacionUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = ParametroEvaluacion
    form_class = ParametroEvaluacionForm
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista de parámetros de evaluación después de editar un parámetro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar parámetro de evaluación {self.object}'
        return context

class ParametroEvaluacionDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = ParametroEvaluacion
    template_name = 'clubes/parametro_evaluacion_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_parametros_evaluacion')  # Redirige a la lista después de eliminar un parámetro de evaluación

class PlanillaExamenDetailView(LoginRequiredMixinConMensaje, ListView):
    model = PlanillaExamen
    template_name = 'clubes/planilla_examen_detail.html'
    context_object_name = 'planillas'  # Nombre del contexto para acceder a las planillas de examen en la plantilla

    def get_queryset(self):
        # Filtra las planillas de examen por el ID del fichaje proporcionado en la URL
        fichaje = self.kwargs.get('fichaje')
        return PlanillaExamen.objects.filter(fichaje=fichaje)

class ResultadoExamenCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = PlanillaExamen
    form_class = ResultadoExamenForm
    success_url = reverse_lazy('clubes:listar_planilla_examen')  # Redirige a la lista de planillas de examen después de crear una planilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear resultado de examen{self.object}'
        return context
    
class ResultadoExamenListView(LoginRequiredMixinConMensaje, ListView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_list.html'
    context_object_name = 'resultados'  # Nombre del contexto para acceder a los resultados de examen en la plantilla

class ResultadoExamenUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = PlanillaExamen
    form_class = ResultadoExamenForm
    success_url = reverse_lazy('clubes:listar_resultados_examen')  # Redirige a la lista de resultados de examen después de editar un resultado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar resultado de examen {self.object}'
        return context

class ResultadoExamenDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_confirm_delete.html'
    success_url = reverse_lazy('clubes:listar_resultados_examen')

class ResultadoExamenDetailView(LoginRequiredMixinConMensaje, ListView):
    model = PlanillaExamen
    template_name = 'clubes/resultado_examen_detail.html'
    context_object_name = 'resultados'  # Nombre del contexto para acceder a los resultados de examen en la plantilla

    def get_queryset(self):
        # Filtra los resultados de examen por el ID del fichaje proporcionado en la URL
        fichaje = self.kwargs.get('fichaje')
        return PlanillaExamen.objects.filter(fichaje=fichaje)


class MetricaRegistradaCreateView(LoginRequiredMixinConMensaje, SharedFormMixin, CreateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de crear una métrica

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Crear métrica registrada{self.object}'
        return context

class MetricaRegistradaDeatilView(LoginRequiredMixinConMensaje, DetailView):
    pass
    
class MetricaRegistradaListView(LoginRequiredMixinConMensaje, ListView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica/metrica_registrada_list.html'
    context_object_name = 'metricas'  # Nombre del contexto para acceder a las métricas registradas en la plantilla

class MetricaRegistradaUpdateView(LoginRequiredMixinConMensaje, SharedFormMixin, UpdateView):
    model = MetricaRegistrada
    form_class = MetricaRegistradaForm
    success_url = reverse_lazy('clubes:listar_metricas_registradas')  # Redirige a la lista de métricas registradas después de editar una métrica

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar métrica registrada {self.object}'
        return context

class MetricaRegistradaDeleteView(LoginRequiredMixinConMensaje, DeleteView):
    model = MetricaRegistrada
    template_name = 'clubes/metrica_registrada_confirm_delete.html'
    success_url = reverse_lazy('clubes:listar_metricas_registradas')