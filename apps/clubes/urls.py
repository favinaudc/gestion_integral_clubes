from django.urls import path, include
from . import views

app_name = 'clubes'

urlpatterns = [
    path('', views.clubes, name='clubes_listado'),
    path('club/<int:club_id>/categorias/', views.categorias, name='club_categorias'),
]