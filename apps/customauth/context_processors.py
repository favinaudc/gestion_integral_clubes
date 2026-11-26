from .models import PerfilClub


def club_admin_context(request):
    club_admin_membresia = None
    if request.user.is_authenticated:
        club_admin_membresia = (
            PerfilClub.objects.filter(
                perfil__usuario=request.user,
                grupo_rol__name='CLUB_ADMIN',
            )
            .select_related('club')
            .first()
        )

    return {'club_admin_membresia': club_admin_membresia}
