from django.urls import path, include
from .views.club_views import *
from .views.ciclos_views import *
from .views.socios_views import *
from .views.entrenador_views import *
from .views.disciplinas_views import *
from .views.categorias_views import *
from .views.fichajes_views import *
from .views.examenes_views import *


app_name = 'clubes'

urlpatterns = [
    path('', ClubListView.as_view(), name='listar_clubes'),
    path('club/create/', ClubCreateView.as_view(), name='crear_club'), 
    path('club/<int:pk>/detalles/', ClubDetailView.as_view(), name='detalles_club'),
    path('club/<int:pk>/editar/', ClubUpdateView.as_view(), name='editar_club'),
    path('club/<int:pk>/eliminar/', ClubDeleteView.as_view(), name='eliminar_club'),
    path('club/<int:pk>/gestionar/', GestionarClubView.as_view() , name='gestionar_club'),
    path('club/<int:pk>/crear-usuario-gestion/', asociar_usuario_club , name='crear_usuario_gestion_club')
]

ciclos_urls = [
    path('ciclos/', CicloListView.as_view(), name='listar_ciclos'),
    path('ciclos/<int:pk>/editar/', CicloUpdateView.as_view(), name='editar_ciclo'),
    path('ciclos/<int:pk>/eliminar/', CicloDeleteView.as_view(), name='eliminar_ciclo'),
    path('ciclos/create/', CicloCreateView.as_view(), name='crear_ciclo'),
]

socios_urls = [
    path('socios/', SocioListView.as_view(), name='listar_socios'),
    path('socios/create/', SocioCreateView.as_view(), name='crear_socio'), 
    path('socios/<int:pk>/editar/', SocioUpdateView.as_view(), name='editar_socio'),
    path('socios/<int:pk>/eliminar/', SocioDeleteView.as_view(), name='eliminar_socio'),
]
entrenadores_urls = [
    path('entrenadores/', EntrenadorListView.as_view(), name='listar_entrenadores'),
    path('entrenadores/<int:pk>/editar/', EntrenadorUpdateView.as_view(), name='editar_entrenador'),
    path('entrenadores/<int:pk>/eliminar/', EntrenadorDeleteView.as_view(), name='eliminar_entrenador'),
    path('entrenadores/create/', EntrenadorCreateView.as_view(), name='crear_entrenador'),
]
disciplinas_urls =[
    path('disciplinas/', DisciplinaListView.as_view(), name='listar_disciplinas'),
    path('disciplinas/<int:pk>/editar/', DisciplinaUpdateView.as_view(), name='editar_disciplina'),
    path('disciplinas/<int:pk>/eliminar/', DisciplinaDeleteView.as_view(), name='eliminar_disciplina'),
    path('disciplinas/create/', DisciplinaCreateView.as_view(), name='crear_disciplina'),
]
categorias_urls =[
    path('categorias/', CategoriaListView.as_view(), name='listar_categorias'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    path('categorias/create/', CategoriaCreateView.as_view(), name='crear_categoria'),  
]
fichaje_urls =[
    path('fichajes/', FichajeListView.as_view(), name='listar_fichajes'), 
    path('fichajes/<int:pk>/editar/', FichajeUpdateView.as_view(), name='editar_fichaje'),
    path('fichajes/<int:pk>/eliminar/', FichajeDeleteView.as_view(), name='eliminar_fichaje'),
    path('fichajes/create/', FichajeCreateView.as_view(), name='crear_fichaje'),
]
parametros_evaluacion_urls =[
    path('parametros_evaluacion/', ParametroEvaluacionListView.as_view(), name='listar_parametros_evaluacion'),
    path('parametros_evaluacion/<int:pk>/editar/', ParametroEvaluacionUpdateView.as_view(), name='editar_parametro_evaluacion'),
    path('parametros_evaluacion/<int:pk>/eliminar/', ParametroEvaluacionDeleteView.as_view(), name='eliminar_parametro_evaluacion'),
    path('parametros_evaluacion/create/', ParametroEvaluacionCreateView.as_view(), name='crear_parametro_evaluacion'),
]
plantillas_examen_urls =[
    path('planillas_examen/', PlanillaExamenListView.as_view(), name='listar_planillas_examen'),
    path('planillas_examen/<int:pk>/editar/', PlanillaExamenUpdateView.as_view(), name='editar_planilla_examen'),
    path('planillas_examen/<int:pk>/eliminar/', PlanillaExamenDeleteView.as_view(), name='eliminar_planilla_examen'),
    path('planillas_examen/create/', PlanillaExamenCreateView.as_view(), name='crear_planilla_examen'),
]
resultados_examen_urls =[
    path('resultados_examen/', ResultadoExamenListView.as_view(), name='listar_resultados_examen'),
    path('resultados_examen/<int:pk>/editar/', ResultadoExamenUpdateView.as_view(), name='editar_resultado_examen'),
    path('resultados_examen/<int:pk>/eliminar/', ResultadoExamenDeleteView.as_view(), name='eliminar_resultado_examen'),
    path('resultados_examen/create/', ResultadoExamenCreateView.as_view(), name='crear_resultado_examen'),
]
metricas_registradas_urls =[
    path('metricas_registradas/', MetricaRegistradaListView.as_view(), name='listar_metricas_registradas'),  
    path('metricas_registradas/<int:pk>/editar/', MetricaRegistradaUpdateView.as_view(), name='editar_metrica_registrada'),
    path('metricas_registradas/<int:pk>/eliminar/', MetricaRegistradaDeleteView.as_view(), name='eliminar_metrica_registrada'),
    path('metricas_registradas/create/', MetricaRegistradaCreateView.as_view(), name='crear_metrica_registrada')
]

urlpatterns += ciclos_urls + socios_urls + entrenadores_urls + disciplinas_urls + categorias_urls +fichaje_urls + parametros_evaluacion_urls + plantillas_examen_urls + resultados_examen_urls + metricas_registradas_urls