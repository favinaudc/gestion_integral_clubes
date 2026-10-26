from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from apps.customauth.models import Usuario

# Create your models here.
# definir classes modelos
#Ciclo, Club, Disciplina, Categoria, Entrenador, Examen, Socio(Usuario, Deportista)

class Ciclo(models.Model):
    año = models.IntegerField(unique=True, validators=[MinValueValidator(2000), MaxValueValidator(date.today().year + 1)])
    #fecha_inicio = models.DateField()
    #fecha_fin = models.DateField()

    def __str__(self):
        return str(self.año)
    
class Disciplina(models.Model):
   
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre de la disciplina")  
    descripcion = models.TextField(help_text="@Ingrese la descripción de la disciplina")
   
    def __str__(self):
        return self.nombre
   

class Club(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    fecha_fundacion = models.DateField()

    disciplinas = models.ManyToManyField(Disciplina, related_name='clubes_suscritos', blank=True)
    ciclos = models.ManyToManyField(Ciclo, through='CicloClub', related_name='clubes_participantes', blank=True)

    def __str__(self):
        return self.nombre    


class CicloClub(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        unique_together = ('club', 'ciclo') 
        verbose_name = "Suscripción a Ciclo"
        verbose_name_plural = "Suscripciones a Ciclos"

    def __str__(self):
        return f"{self.club.nombre} - Ciclo {self.ciclo.año}"


class Socio(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='socio', null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    es_deportista = models.BooleanField(default=False, help_text="@Indica si el socio es deportista o no")   
    es_tutor = models.BooleanField(default=False, help_text="@Indica si el socio es tutor o no")
    apto_medico = models.BooleanField(default=False, help_text="@Indica si el socio tiene apto médico o no")
    tutor_responsable = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, help_text="@Ingrese el tutor responsable del socio")

    def __str__(self):
        if self.usuario_id is None:
            return f"Socio #{self.pk}" if self.pk is not None else "Socio sin usuario"
        return str(self.usuario)
    
    @property
    def es_menor_edad(self):
        if not self.usuario.perfil.fecha_nacimiento:
            raise ValueError('Debe definir fecha de nacimiento.')
        hoy = date.today()
        edad = (
            hoy.year
            - self.usuario.perfil.fecha_nacimiento.year
            -(
                (hoy.month, hoy.day)
                <(self.usuario.perfil.fecha_nacimiento.month, self.usuario.perfil.fecha_nacimiento.day)
            )
        )
        return edad < 18
    
    def save(self, *args, **kwargs):
        if self.es_menor_edad:
            if self.tutor_responsable is None:
                raise ValueError('Al ser menos de edad debe tener responsable/tutor asociado.')
        super().save(*args, **kwargs)
    

class Entrenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    club = models.ManyToManyField(Club, related_name='entrenadores')
    experiencia = models.IntegerField(validators=[MinValueValidator(0)], help_text="@Ingrese la cantidad de años de experiencia del entrenador")

    def __str__(self):
        return f"{self.usuario.perfil.nombre} {self.usuario.perfil.apellido}"   


class Categoria(models.Model):
   
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre de la categoría")
    descripcion = models.TextField(help_text="@Ingrese la descripción de la categoría")
    edad_minima = models.IntegerField(validators=[MinValueValidator(0)], help_text="@Ingrese la edad mínima de la categoría")
    edad_maxima = models.IntegerField(validators=[MinValueValidator(0)], help_text="@Ingrese la edad máxima de la categoría")
    club = models.ManyToManyField(Club)
    disciplina = models.ManyToManyField(Disciplina)

    def __str__(self):
        return self.nombre  
    
    def save(self, *args, **kwargs):
        if self.edad_minima >= self.edad_maxima:
            raise ValueError('La edad mínima no puede ser mayor o igual que la edad máxima.')
        
        super().save(*args, **kwargs)

class Fichaje(models.Model):
  
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='fichajes')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_fichaje = models.DateField(help_text="@Ingrese la fecha de fichaje del socio")
    is_active = models.BooleanField(default=True, help_text="@Indica si el fichaje está activo o no")
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)

    def save(self, *args,**kwargs):
        super().save(*args, **kwargs)

        if self.socio and not self.socio.es_deportista:
            self.socio.es_deportista = True
            self.socio.save(update_fields=['es_deportista'])

    def __str__(self):
        return f"{self.socio.usuario.perfil.nombre} {self.socio.usuario.perfil.apellido} - {self.disciplina.nombre} - {self.categoria.nombre} - {self.ciclo.año}" 

class ParametroEvaluacion(models.Model):
   
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre del parámetro de evaluación")
    unidad_medida = models.CharField(max_length=200, help_text="@Ingrese la unidad de medida del parámetro de evaluación")
    tipo_dato = models.CharField(max_length=100, help_text="@Ingrese el tipo de dato del parámetro de evaluación")

    def __str__(self):
        return self.nombre

class PlanillaExamen(models.Model):
    
    fichaje = models.ForeignKey(Fichaje, on_delete=models.CASCADE)
    fecha_examen = models.DateField(help_text="@Ingrese la fecha del examen")
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre del examen")
    diciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    parametro = models.ManyToManyField(ParametroEvaluacion)
    #resultado = models.CharField(max_length=100, help_text="@Ingrese el resultado del examen")
    #observaciones = models.TextField(help_text="@Ingrese las observaciones del examen", blank=True, null=True)

    def __str__(self):
        return f"{self.fichaje.socio.usuario.perfil.nombre} {self.fichaje.socio.usuario.perfil.apellido} - {self.fichaje.disciplina.nombre} - {self.fichaje.categoria.nombre} - {self.fecha_examen}"    

class ResultadoExamen(models.Model):
   
    planilla = models.ForeignKey(PlanillaExamen, on_delete=models.CASCADE)
    fecha_test = models.DateField(help_text="@Ingrese la fecha del resultado del examen")
    valor = models.CharField(max_length=100, help_text="@Ingrese el valor del resultado del examen")
    observaciones = models.TextField(help_text="@Ingrese las observaciones del resultado del examen", blank=True, null=True)

    def __str__(self):
        return f"{self.planilla.fichaje.socio.usuario.perfil.nombre} {self.planilla.fichaje.socio.usuario.perfil.apellido} - {self.planilla.fichaje.disciplina.nombre} - {self.planilla.fichaje.categoria.nombre} - {self.planilla.fecha_examen} - {self.fecha_test}"

class MetricaRegistrada(models.Model):

    resultado = models.ForeignKey(ResultadoExamen, on_delete=models.CASCADE)
    parametro = models.ForeignKey(ParametroEvaluacion, on_delete=models.CASCADE)
    valor_entero = models.IntegerField(help_text="@Ingrese el valor de la métrica registrada",null=True, blank=True)
    valor_decimal = models.DecimalField(max_digits=10, decimal_places=2, help_text="@Ingrese el valor de la métrica registrada",null=True, blank=True)
    valor_tiempo = models.DurationField(help_text="@Ingrese el valor de la métrica registrada",null=True, blank=True)
    observaciones = models.TextField(help_text="@Ingrese las observaciones de la métrica registrada", blank=True, null=True)

    def __str__(self):
        return f"{self.resultado.planilla.fichaje.socio.usuario.perfil.nombre} {self.resultado.planilla.fichaje.socio.usuario.perfil.apellido} - {self.resultado.planilla.fichaje.disciplina.nombre} - {self.resultado.planilla.fichaje.categoria.nombre} - {self.resultado.planilla.fecha_examen} - {self.parametro.nombre} - {self.valor}"    