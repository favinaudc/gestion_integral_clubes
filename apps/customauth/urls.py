from django.urls import path, include
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('cambiar-rol/<int:pk>', views.cambiar_rol, name='cambiar_rol'),
    path('perfil/editar/', views.PerfilUpdateView.as_view(), name='editar_perfil'),
]