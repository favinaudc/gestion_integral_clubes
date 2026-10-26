from django.shortcuts import redirect, render
from apps.customauth.models import PerfilClub
from django.contrib import messages


def home_resolver(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('clubes:listar_clubes')
        
        if request.user.is_club_admin or request.user.is_club_administrativo:
            suscripcion_admin = PerfilClub.objects.filter(
                perfil__usuario=request.user, 
                grupo_rol__name='CLUB_ADMIN'
            ).first()
            
            if suscripcion_admin and suscripcion_admin.club:
                return redirect('clubes:gestionar_club', pk=suscripcion_admin.club.pk)
            else:
                messages.error(request, "Aún no tiene un club asignado")
                return redirect('clubes:listar_clubes') 
        
        if request.user.is_usuario:
            return render(request, 'home_user.html')
            
    # Redirección por defecto si algo falla o si recién se loguea sin un rol definido aún
    return render(request, 'home_user.html')
        