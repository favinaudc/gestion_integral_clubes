from functools import wraps
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

def login_required_con_mensaje(view_func):
    """
    Decorador para Vistas Basadas en Funciones que exige inicio de sesión y 
    envía un mensaje tipo Toast/Alerta si el usuario no está autenticado.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # error piolaso
            messages.error(request, "Debe iniciar sesión para acceder a esta sección.")
            # redirigimos al login (esto usa automáticamente la LOGIN_URL de settings.py)
            # request.get_full_path() guarda la ruta que el usuario intentó visitar en el parámetro ?next=
            return redirect_to_login(request.get_full_path())
            
        # si está autenticado, la vista sigue su curso normal
        return view_func(request, *args, **kwargs)
        
    return _wrapped_view


def rol_required(grupos_roles):
    """
    Decorador que verifica el grupo_activo directo del Usuario.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            
            # usamos la property get_grupo_activo del Usuario
            grupo_usuario = request.user.get_grupo_activo 
            
            # verificamos si ese grupo está en la lista de permitidos
            if grupo_usuario not in grupos_roles:
                # mensaje Toastify
                messages.error(request, "No tenés los roles ó permisos necesarios para acceder a esta sección.")
                # redirigimos al login
                return redirect_to_login(request.get_full_path())
                
            # si el grupo coincide, la vista sigue su curso normal
            return view_func(request, *args, **kwargs)
            
        return _wrapped_view
    return decorator