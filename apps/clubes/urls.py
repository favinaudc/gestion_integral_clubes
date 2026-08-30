from django.urls import path, include
from . import views

app_name = 'clubes'

urlpatterns = [
    path('', views.clubes, name='list'),
    path('club/<int:club_id>/categorias/', views.categorias, name='categorias'),
]