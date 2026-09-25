from django.db import models

# Create your models here.
class Usuario(models.Model):
    cuit_cuil = models.CharField(max_length=11, unique=True, help_text="@Ingrese el CUIT/CUIL del usuario")
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre del usuario")
    apellido = models.CharField(max_length=100, help_text="@Ingrese el apellido del usuario")
    email = models.EmailField(help_text="@Ingrese el correo electrónico del usuario")
    is_active = models.BooleanField(default=True, help_text="@Indica si el usuario está activo o no")
    is_staff = models.BooleanField(default=False, help_text="@Indica si el usuario es staff o no")
    #telefono = models.CharField(max_length=15, help_text="@Ingrese el teléfono del usuario")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"