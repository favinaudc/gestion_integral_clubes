from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Carga de elementos iniciales del sistema.'

    def handle(self, *args, **kwargs):

        grupos_base = [
            'USUARIO',
            'ADMIN',
            'CLUB_ADMIN',
            'CLUB_ADMINISTRATIVO',
            'ENTRENADOR',
            'SOCIO'
        ]

        self.stdout.write('Iniciando carga...')
        self.stdout.write('Grupos...')

        for nombre in grupos_base:
            grupo, creado = Group.objects.get_or_create(name=nombre)
            if creado:
                self.stdout.write(self.style.SUCCESS(f'+ Grupo creado: {nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'- El grupo ya existía: {nombre}'))

        self.stdout.write(self.style.SUCCESS('Carga de grupos finalizada.'))

        grupo_admin = Group.objects.get(name='ADMIN')
        codenames_admin = [
            'view_ciclo', 'add_ciclo',
            'view_club', 'add_club', 'change_club', 'delete_club', 'asignar_usuario_gestion',
            'view_disciplina', 'add_disciplina', 'change_disciplina', 'delete_disciplina',
        ]

        permisos = Permission.objects.filter(content_type__app_label='clubes', codename__in=codenames_admin)
        grupo_admin.permissions.set(permisos)

        grupo_club_admin = Group.objects.get(name='CLUB_ADMIN')
        codenames_club_admin = [
            'view_ciclo', 'suscribirse_a_ciclo',
            'gestionar_club',
            'view_disciplina', 'suscribir_club_a_disciplina',
        ]

        permisos_club_admin = Permission.objects.filter(content_type__app_label='clubes', codename__in=codenames_club_admin)
        grupo_club_admin.permissions.set(permisos_club_admin)

