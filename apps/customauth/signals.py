from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Usuario

'''
Las signals (señales) en Django implementan el patrón de diseño Observador (Observer). 
Permiten que diferentes partes desacopladas de la aplicación "escuchen" 
y reaccionen cuando ocurren eventos específicos en otro lugar del sistema.

El archivo signals.py centraliza la captura de estos eventos. 
Su funcionamiento se basa en tres componentes:

Sender (Emisor): El modelo que realiza la acción (en este caso, Usuario).

Signal (Señal): El evento en sí. post_save es una señal nativa de Django 
que se dispara automáticamente justo después de que se ejecuta un INSERT o UPDATE en la base de datos.

Receiver (Receptor): La función decorada (ej. asignar_rol_por_defecto). 
Al usar @receiver(post_save, sender=Usuario), la función se queda esperando. 
Cada vez que se guarda un usuario, la señal dispara la función, evalúa el flag created (que es True solo si es un INSERT nuevo) 
y ejecuta la asignación del grupo sin acoplar código dentro de las vistas o formularios.
'''

@receiver(post_save, sender=Usuario)
def asignar_rol_por_defecto(sender, instance, created, **kwargs):
    if created:
        # Obtiene o crea el grupo 'usuario'
        grupo_base, _ = Group.objects.get_or_create(name='USUARIO')
        
        # Lo añade a la relación ManyToMany de PermissionsMixin
        instance.groups.add(grupo_base)
        
        # Lo setea como su grupo activo por defecto
        instance.grupo_activo = grupo_base
        instance.save(update_fields=['grupo_activo'])