from django.urls import path, include
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]