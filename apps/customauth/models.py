from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group

# 1. El Manager Personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, cuit_cuil, password=None, **extra_fields):
        if not cuit_cuil:
            raise ValueError('El usuario debe tener un CUIT/CUIL válido')
        
        # Normalizamos el email si es que se proporciona
        if 'email' in extra_fields:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(
            cuit_cuil=cuit_cuil,
            **extra_fields
        )
        user.set_password(password) # Encripta la contraseña[cite: 5]
        user.save(using=self._db)
        return user

    def create_superuser(self, cuit_cuil, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(cuit_cuil, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    cuit_cuil = models.CharField(max_length=11, unique=True, help_text="Ingrese el CUIT/CUIL del usuario sin guiones")        
    email = models.EmailField(unique=True, null=False, blank=False)
    
    is_active = models.BooleanField(default=True, help_text="Indica si el usuario está activo o no")
    is_staff = models.BooleanField(default=False, help_text="Indica si el usuario es staff (Administrador) o no")
    grupo_activo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UsuarioManager()

    # Configuraciones clave para Django Auth
    USERNAME_FIELD = 'cuit_cuil'  # Define que se inicia sesión con CUIT/CUIL
    REQUIRED_FIELDS = ['email'] # Campos extra que exigirá la terminal al hacer createsuperuser

    def __str__(self):
        return f"{self.cuit_cuil}"

    @property
    def get_grupo_activo(self):
        if self.grupo_activo:
            return self.grupo_activo.name.upper()
        return ''

    @property
    def is_admin(self):
        return self.get_grupo_activo == 'ADMIN'

    @property
    def is_club_admin(self):
        return self.get_grupo_activo == 'CLUB_ADMIN'

    @property
    def is_club_administrativo(self):
        return self.get_grupo_activo == 'CLUB_ADMINISTRATIVO'

    @property
    def is_entrenador(self):
        return self.get_grupo_activo == 'ENTRENADOR'

    @property
    def is_socio(self):
        return self.get_grupo_activo == 'SOCIO'

    @property
    def is_usuario(self):
        return self.get_grupo_activo == 'USUARIO'


class Perfil(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ingrese el nombre del usuario")
    apellido = models.CharField(max_length=50, help_text="Ingrese el apellido del usuario")
    fecha_nacimiento = models.DateField(help_text="Ingrese la fecha de nacimiento del usuario")
    telefono = models.CharField(max_length=20, null=True, blank=True, help_text="Ingrese el teléfono del usuario (opcional)")
    direccion = models.CharField(max_length=100, null=True, blank=True, help_text="Ingrese la dirección del usuario (opcional)")
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    club = models.ManyToManyField('clubes.Club', through='PerfilClub', related_name='perfiles', blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class PerfilClub(models.Model):
    fecha_asociacion = models.DateField(auto_now_add=True)
    
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    club = models.ForeignKey('clubes.Club', on_delete=models.CASCADE)
    grupo_rol = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    # class Meta:
    #    unique_together = ('perfil', 'club')

    def __str__(self):
        return f"{self.perfil} - {self.club}"