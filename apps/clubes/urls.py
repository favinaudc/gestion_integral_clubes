from django.urls import path, include
from . import views

app_name = 'clubes'

urlpatterns = [
    path('', views.clubes, name='list'),
    path('club/<int:club_id>/categorias/', views.categorias, name='categorias'),
    path('ciclos/', views.CicloListView.as_view(), name='listar_ciclos'),
    
    path('ciclos/<int:pk>/editar/', views.CicloUpdateView.as_view(), name='editar_ciclo'),
    path('ciclos/<int:pk>/eliminar/', views.CicloDeleteView.as_view(), name='eliminar_ciclo'),
    path('ciclos/create/', views.CicloCreateView.as_view(), name='crear_ciclo'),
    path('clubes/', views.ClubListView.as_view(), name='listar_clubes'),
    path('clubes/<int:pk>/editar/', views.ClubUpdateView.as_view(), name='editar_club'),
    path('clubes/<int:pk>/eliminar/', views.ClubDeleteView.as_view(), name='eliminar_club'),
    path('clubes/create/', views.ClubCreateView.as_view(), name='crear_club'), 
    path('socios/', views.SocioListView.as_view(), name='listar_socios'),
    path('socios/<int:pk>/editar/', views.SocioUpdateView.as_view(), name='editar_socio'),
    path('socios/<int:pk>/eliminar/', views.SocioDeleteView.as_view(), name='eliminar_socio'),
    path('socios/create/', views.SocioCreateView.as_view(), name='crear_socio'), 
    path('entrenadores/', views.EntrenadorListView.as_view(), name='listar_entrenadores'),
    path('entrenadores/<int:pk>/editar/', views.EntrenadorUpdateView.as_view(), name='editar_entrenador'),
    path('entrenadores/<int:pk>/eliminar/', views.EntrenadorDeleteView.as_view(), name='eliminar_entrenador'),
    path('entrenadores/create/', views.EntrenadorCreateView.as_view(), name='crear_entrenador'),
    path('disciplinas/', views.DisciplinaListView.as_view(), name='listar_disciplinas'),
    path('disciplinas/<int:pk>/editar/', views.DisciplinaUpdateView.as_view(), name='editar_disciplina'),
    path('disciplinas/<int:pk>/eliminar/', views.DisciplinaDeleteView.as_view(), name='eliminar_disciplina'),
    path('disciplinas/create/', views.DisciplinaCreateView.as_view(), name='crear_disciplina'),
    path('categorias/', views.CategoriaListView.as_view(), name='listar_categorias'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    path('categorias/create/', views.CategoriaCreateView.as_view(), name='crear_categoria'),    
    path('fichajes/', views.FichajeListView.as_view(), name='listar_fichajes'), 
    path('fichajes/<int:pk>/editar/', views.FichajeUpdateView.as_view(), name='editar_fichaje'),
    path('fichajes/<int:pk>/eliminar/', views.FichajeDeleteView.as_view(), name='eliminar_fichaje'),
    path('fichajes/create/', views.FichajeCreateView.as_view(), name='crear_fichaje'),
    path('parametros_evaluacion/', views.ParametroEvaluacionListView.as_view(), name='listar_parametros_evaluacion'),
    path('parametros_evaluacion/<int:pk>/editar/', views.ParametroEvaluacionUpdateView.as_view(), name='editar_parametro_evaluacion'),
    path('parametros_evaluacion/<int:pk>/eliminar/', views.ParametroEvaluacionDeleteView.as_view(), name='eliminar_parametro_evaluacion'),
    path('parametros_evaluacion/create/', views.ParametroEvaluacionCreateView.as_view(), name='crear_parametro_evaluacion'),
    path('planillas_examen/', views.PlanillaExamenListView.as_view(), name='listar_planillas_examen'),
    path('planillas_examen/<int:pk>/editar/', views.PlanillaExamenUpdateView.as_view(), name='editar_planilla_examen'),
    path('planillas_examen/<int:pk>/eliminar/', views.PlanillaExamenDeleteView.as_view(), name='eliminar_planilla_examen'),
    path('planillas_examen/create/', views.PlanillaExamenCreateView.as_view(), name='crear_planilla_examen'),
    path('resultados_examen/', views.ResultadoExamenListView.as_view(), name='listar_resultados_examen'),
    path('resultados_examen/<int:pk>/editar/', views.ResultadoExamenUpdateView.as_view(), name='editar_resultado_examen'),
    path('resultados_examen/<int:pk>/eliminar/', views.ResultadoExamenDeleteView.as_view(), name='eliminar_resultado_examen'),
    path('resultados_examen/create/', views.ResultadoExamenCreateView.as_view(), name='crear_resultado_examen'),
    path('metricas_registradas/', views.MetricaRegistradaListView.as_view(), name='listar_metricas_registradas'),  
    path('metricas_registradas/<int:pk>/editar/', views.MetricaRegistradaUpdateView.as_view(), name='editar_metrica_registrada'),
    path('metricas_registradas/<int:pk>/eliminar/', views.MetricaRegistradaDeleteView.as_view(), name='eliminar_metrica_registrada'),
    path('metricas_registradas/create/', views.MetricaRegistradaCreateView.as_view(), name='crear_metrica_registrada')
     
    
]