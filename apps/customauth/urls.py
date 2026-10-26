from django.urls import path, include
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('cambiar-rol/<int:pk>', views.cambiar_rol, name='cambiar_rol'),
]