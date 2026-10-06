from django.urls import path, include
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
]