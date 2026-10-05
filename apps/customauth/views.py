from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    # Si el usuario ya está logueado, lo mandamos directo al panel
    if request.user.is_authenticated:
        return redirect('clubes:listar_clubes') # Cambiá esto por la URL de tu home/dashboard

    if request.method == 'POST':
        # Capturamos los datos que vienen del input del HTML
        cuit = request.POST.get('cuit_cuil')
        password = request.POST.get('password')

        # authenticate() verifica en la base de datos si las credenciales coinciden
        # Usamos cuit_cuil porque lo definiste como USERNAME_FIELD en tu modelo
        user = authenticate(request, cuit_cuil=cuit, password=password)

        if user is not None:
            # Si el usuario existe y está activo, creamos la sesión
            login(request, user)
            return redirect('clubes:listar_clubes') # TODO: Ésto debe cambiar dependiendo del ROL/GROUP del usuario
        else:
            # Si falla, enviamos un mensaje de error a la plantilla
            messages.error(request, "El CUIT/CUIL o la contraseña son incorrectos.")

    # Si la petición es GET (solo entrar a la página), renderizamos el formulario
    return render(request, 'customauth/login.html')


def cerrar_sesion(request):
    # Destruye la sesión actual del usuario
    logout(request)
    
    # Opcional: le mandamos un mensajito de despedida
    messages.info(request, "Has cerrado sesión exitosamente.")
    
    # Lo redirigimos de vuelta a la pantalla de login
    return redirect('auth:login')