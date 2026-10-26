from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'customauth/login.html'
    
    # Equivalente a tu "if request.user.is_authenticated: return redirect('home')"
    redirect_authenticated_user = True  
    
    def get_success_url(self):
        # Redirección tras un login exitoso
        return reverse_lazy('home') # Cambiá 'home' por el namespace:name correspondiente
        
    def form_invalid(self, form):
        # Equivalente al bloque "else" cuando falla el authenticate()
        messages.error(self.request, "El CUIT/CUIL o la contraseña son incorrectos.")
        return super().form_invalid(form)


def cerrar_sesion(request):
    logout(request)
    
    messages.success(request, "Has cerrado sesión exitosamente.")
    
    # Lo redirigimos de vuelta a la pantalla de login
    return redirect('auth:login')

def cambiar_rol(request, pk):

    grupo_solicitado = Group.objects.get(pk=pk)
    if request.user.groups.filter(pk=grupo_solicitado.pk).exists():
        request.user.grupo_activo = grupo_solicitado
        request.user.save()
        messages.success(request, 'Rol actualizado')
    return redirect('home')