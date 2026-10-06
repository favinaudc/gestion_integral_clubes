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
    email = models.EmailField(unique=True, null=True, blank=True)
    
    is_active = models.BooleanField(default=True, help_text="Indica si el usuario está activo o no")
    is_staff = models.BooleanField(default=False, help_text="Indica si el usuario es staff (Administrador) o no")
    grupo_activo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UsuarioManager()

    # Configuraciones clave para Django Auth
    USERNAME_FIELD = 'cuit_cuil'  # Define que se inicia sesión con CUIT/CUIL
    REQUIRED_FIELDS = ['email'] # Campos extra que exigirá la terminal al hacer createsuperuser

    def __str__(self):
        return f"{self.cuit_cuil}"