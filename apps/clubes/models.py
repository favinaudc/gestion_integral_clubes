from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from apps.customauth.models import Usuario

# Create your models here.
# definir classes modelos
#Ciclo, Club, Disciplina, Categoria, Entrenador, Examen, Socio(Usuario, Deportista)

class Ciclo(models.Model):
    año = models.IntegerField(unique=True, validators=[MinValueValidator(2000), MaxValueValidator(date.today().year + 1)])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return str(self.año)
    
class Club(models.Model):
   
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    fecha_fundacion = models.DateField()

    def __str__(self):
        return self.nombre    



class Socio(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE )
    fecha_nacimiento = models.DateField(help_text="@Ingrese la fecha de nacimiento del usuario")
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    es_deportista = models.BooleanField(default=False, help_text="@Indica si el socio es deportista o no")   
    es_tutor = models.BooleanField(default=False, help_text="@Indica si el socio es tutor o no")
    apto_medico = models.BooleanField(default=False, help_text="@Indica si el socio tiene apto médico o no")
    tutor_responsable_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, help_text="@Ingrese el tutor responsable del socio")

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"
    
class Entrenador(models.Model):
   
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    club_id = models.ManyToManyField(Club, related_name='entrenadores')
    # volver a agregar los related_name para poder acceder Qué problema ayudan a resolver select_related() y prefetch_related()
    #especialidad = models.CharField(max_length=100, help_text="@Ingrese la especialidad del entrenador")
    experiencia = models.IntegerField(validators=[MinValueValidator(0)], help_text="@Ingrese la cantidad de años de experiencia del entrenador")

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"   
class Disciplina(models.Model):
   
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre de la disciplina")  
    descripcion = models.TextField(help_text="@Ingrese la descripción de la disciplina")
    club_id = models.ManyToManyField(Club, related_name='disciplinas')
    entrenador_id = models.ManyToManyField(Entrenador, related_name='disciplinas'  )

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
   
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre de la categoría")
    descripcion = models.TextField(help_text="@Ingrese la descripción de la categoría")
    edad_minima = models.IntegerField(validators=[MinValueValidator(0)], help_text="@Ingrese la edad mínima de la categoría")
    edad_maxima = models.IntegerField(validators=[MinValueValidator(0)], help_text="@Ingrese la edad máxima de la categoría")
    club_id = models.ManyToManyField(Club)
    disciplina_id = models.ManyToManyField(Disciplina)

    def __str__(self):
        return self.nombre    

class Fichaje(models.Model):
  
    socio_id = models.ForeignKey(Socio, on_delete=models.CASCADE)
    disciplina_id = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_fichaje = models.DateField(help_text="@Ingrese la fecha de fichaje del socio")
    is_active = models.BooleanField(default=True, help_text="@Indica si el fichaje está activo o no")
    ciclo_id = models.ForeignKey(Ciclo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.socio_id.usuario.nombre} {self.socio_id.usuario.apellido} - {self.disciplina_id.nombre} - {self.categoria_id.nombre} - {self.ciclo_id.año}" 

class ParametroEvaluacion(models.Model):
   
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre del parámetro de evaluación")
    unidad_medida = models.CharField(max_length=200, help_text="@Ingrese la unidad de medida del parámetro de evaluación")
    tipo_dato = models.CharField(max_length=100, help_text="@Ingrese el tipo de dato del parámetro de evaluación")

    def __str__(self):
        return self.nombre

class PlanillaExamen(models.Model):
    
    fichaje_id = models.ForeignKey(Fichaje, on_delete=models.CASCADE)
    fecha_examen = models.DateField(help_text="@Ingrese la fecha del examen")
    nombre = models.CharField(max_length=100, help_text="@Ingrese el nombre del examen")
    diciplina_id = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    parametro_id = models.ManyToManyField(ParametroEvaluacion)
    #resultado = models.CharField(max_length=100, help_text="@Ingrese el resultado del examen")
    #observaciones = models.TextField(help_text="@Ingrese las observaciones del examen", blank=True, null=True)

    def __str__(self):
        return f"{self.fichaje_id.socio_id.usuario.nombre} {self.fichaje_id.socio_id.usuario.apellido} - {self.fichaje_id.disciplina_id.nombre} - {self.fichaje_id.categoria_id.nombre} - {self.fecha_examen}"    

class ResultadoExamen(models.Model):
   
    planilla_id = models.ForeignKey(PlanillaExamen, on_delete=models.CASCADE)
    fecha_test = models.DateField(help_text="@Ingrese la fecha del resultado del examen")
    valor = models.CharField(max_length=100, help_text="@Ingrese el valor del resultado del examen")
    observaciones = models.TextField(help_text="@Ingrese las observaciones del resultado del examen", blank=True, null=True)

    def __str__(self):
        return f"{self.planilla_id.fichaje_id.socio_id.usuario.nombre} {self.planilla_id.fichaje_id.socio_id.usuario.apellido} - {self.planilla_id.fichaje_id.disciplina_id.nombre} - {self.planilla_id.fichaje_id.categoria_id.nombre} - {self.planilla_id.fecha_examen} - {self.fecha_test}"

class MetricaRegistrada(models.Model):

    resultado_id = models.ForeignKey(ResultadoExamen, on_delete=models.CASCADE)
    parametro_id = models.ForeignKey(ParametroEvaluacion, on_delete=models.CASCADE)
    valor_entero = models.IntegerField(help_text="@Ingrese el valor de la métrica registrada",null=True, blank=True)
    valor_decimal = models.DecimalField(max_digits=10, decimal_places=2, help_text="@Ingrese el valor de la métrica registrada",null=True, blank=True)
    valor_tiempo = models.DurationField(help_text="@Ingrese el valor de la métrica registrada",null=True, blank=True)
    observaciones = models.TextField(help_text="@Ingrese las observaciones de la métrica registrada", blank=True, null=True)

    def __str__(self):
        return f"{self.resultado_id.planilla_id.fichaje_id.socio_id.usuario.nombre} {self.resultado_id.planilla_id.fichaje_id.socio_id.usuario.apellido} - {self.resultado_id.planilla_id.fichaje_id.disciplina_id.nombre} - {self.resultado_id.planilla_id.fichaje_id.categoria_id.nombre} - {self.resultado_id.planilla_id.fecha_examen} - {self.parametro_id.nombre} - {self.valor}"    