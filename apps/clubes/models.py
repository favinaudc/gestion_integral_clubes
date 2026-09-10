from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

# Create your models here.
# definir classes modelos
#Ciclo, Club, Disciplina, Categoria, Entrenador, Examen, Socio(Usuario, Deportista)

class Ciclo(models.Model):
    año = models.CharField(max_length=4, validators=[MinValueValidator(2000), MaxValueValidator(date.today().year + 1)], help_text="Ingrese el año del ciclo")
    fecha_inicio = models.DateField(validators=[MinValueValidator(date.today().year)], help_text="Ingrese la fecha de inicio del ciclo"    )
    fecha_fin = models.DateField(validators=[MaxValueValidator(date.today().year + 1)], help_text="Ingrese la fecha de fin del ciclo")

    def __str__(self):
        return self.año
    