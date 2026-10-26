from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        # Capturamos los datos que vienen del input del HTML
        cuit = request.POST.get('cuit_cuil')
        password = request.POST.get('password')

        user = authenticate(request, cuit_cuil=cuit, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Si falla, enviamos un mensaje de error a la plantilla
            messages.error(request, "El CUIT/CUIL o la contraseña son incorrectos.")

    return render(request, 'customauth/login.html')


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