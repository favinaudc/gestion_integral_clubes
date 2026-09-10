from django.db import models

class Usuario(models.Model):
    cuit_cuil = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Club(models.Model):
    nombre = models.CharField(max_length=150)
    cuit = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Socio(models.Model):
    usuario_cuit = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    es_deportista = models.BooleanField(default=False)
    es_tutor = models.BooleanField(default=False)
    apto_medico = models.BooleanField(default=False)
    tutor_responsable = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='tutelados')

    def __str__(self):
        return f"Socio: {self.usuario_cuit}"

class Entrenador(models.Model):
    usuario_cuit = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entrenador: {self.usuario_cuit}"

class Disciplina(models.Model):
    nombre = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    edad_minima = models.IntegerField()
    edad_maxima = models.IntegerField()
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.disciplina})"

class Ciclo(models.Model):
    anio = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.anio)

class Fichaje(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fichaje: {self.socio} - {self.disciplina}"

class PlantillaExamen(models.Model):
    nombre = models.CharField(max_length=150)
    es_activo = models.BooleanField(default=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ParametroEvaluacion(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=50)
    tipo_dato = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class ResultadoExamen(models.Model):
    fecha_test = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    fichaje = models.ForeignKey(Fichaje, on_delete=models.CASCADE)
    plantilla = models.ForeignKey(PlantillaExamen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Examen {self.fecha_test} - {self.fichaje}"

class MetricaRegistrada(models.Model):
    valor_entero = models.IntegerField(null=True, blank=True)
    valor_decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_tiempo = models.DurationField(null=True, blank=True) # Mapea a un "interval" en BD
    resultado_examen = models.ForeignKey(ResultadoExamen, on_delete=models.CASCADE)
    parametro = models.ForeignKey(ParametroEvaluacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Métrica de {self.parametro}"