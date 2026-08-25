from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:club_id>/categorias/', views.categorias, name='categorias'),
]