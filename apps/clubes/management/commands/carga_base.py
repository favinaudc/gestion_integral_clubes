from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

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