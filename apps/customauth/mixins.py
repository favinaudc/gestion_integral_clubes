from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from .models import PerfilClub

class ValidarRolClubMixin:
    """
    Verifica que el usuario logueado tenga un rol específico en el Club al que intenta acceder.
    Se asume que la URL captura el ID del club como 'pk' o 'club_id'.
    """
    rol_requerido = []  # Debe ser definido en la vista que herede este mixin

    def dispatch(self, request, *args, **kwargs):
        # 1. Obtener el ID del club desde la URL (Asegurate de que coincida con tu urls.py)
        club_id = self.kwargs.get('pk') or self.kwargs.get('club_id')
        
        # 2. Verificar si existe la relación en la tabla intermedia
        tiene_permiso = PerfilClub.objects.filter(
            perfil__usuario=request.user,
            club_id=club_id,
            grupo_rol__name__in=self.rol_requerido
        ).exists()

        if not tiene_permiso or request.user.grupo_activo.name not in self.rol_requerido:
            messages.error(request, "No tienes permisos de gestión ó consulta para este club.")
            return redirect('home')  # Redirige a la página de inicio o a otra página de tu elección
            
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixinConMensaje(LoginRequiredMixin):
    """
    Mixin personalizado que exige inicio de sesión y envía un mensaje 
    tipo Toast/Alerta al usuario si intenta acceder sin estar autenticado.
    """
    def handle_no_permission(self):
        # Inyectamos el mensaje antes de que se produzca la redirección
        messages.error(self.request, "Debe iniciar sesión para acceder a esta sección.")
        
        # Ejecutamos el comportamiento original (Redirigir al login)
        return super().handle_no_permission()


class RolRequeridoMixin(AccessMixin):
    """
    Mixin que verifica el grupo_activo directo del Usuario.
    """
    rol_requerido = [] # Se define en la vista

    def dispatch(self, request, *args, **kwargs):
        # Primero nos aseguramos que esté autenticado
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        # Usamos tu property get_grupo_activo
        grupo_usuario = request.user.get_grupo_activo
        
        # Comparamos
        if grupo_usuario not in self.rol_requerido:
            messages.error(request, "No tenés los permisos necesarios para acceder a esta sección.")
            return redirect('home') # Cambiá por el nombre de tu ruta
            
        return super().dispatch(request, *args, **kwargs)