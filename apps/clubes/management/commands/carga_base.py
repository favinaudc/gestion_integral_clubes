from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Comman(BaseCommand):
    help = 'Carga de elementos iniciales del sistema.'

    def handle(self, *args, **kwargs):

        grupos_base = [
            'admin',
            'club_admin',
            'club_administrativo',
            'entrenador',
            'socio',
            'usuario'
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