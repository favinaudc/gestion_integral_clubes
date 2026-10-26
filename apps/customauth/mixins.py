from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
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

        if not tiene_permiso:
            messages.error(request, "No tienes permisos de gestión ó consulta para este club.")
            return redirect('clubes:listar_clubes')  # Redirige a la página de inicio o a otra página de tu elección
            
        return super().dispatch(request, *args, **kwargs)