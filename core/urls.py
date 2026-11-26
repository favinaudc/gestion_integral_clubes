"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_resolver
from apps.clubes.views.entrenador_views import (
    EntrenadorCategoriasView,
    EntrenadorFichajesView,
    EntrenadorHomeView,
)


urlpatterns = [
    path('', include('apps.web.urls')),  # Ruta raíz que redirige a las URLs de la aplicación "clubes"
    path('admin/', admin.site.urls),
    path('clubes/', include('apps.clubes.urls')),
    path('auth/', include('apps.customauth.urls')),
    path('entrenador/', EntrenadorHomeView.as_view(), name='entrenador_home'),
    path(
        'entrenador/club/<int:club_pk>/disciplina/<int:disciplina_pk>/',
        EntrenadorCategoriasView.as_view(),
        name='entrenador_categorias',
    ),
    path(
        'entrenador/club/<int:club_pk>/disciplina/<int:disciplina_pk>/categoria/<int:categoria_pk>/',
        EntrenadorFichajesView.as_view(),
        name='entrenador_fichajes',
    ),
    path('home/', home_resolver, name='home'),  # Ruta para la vista de inicio
]
