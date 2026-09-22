import django_tables2 as tables
from .models import Club, Ciclo, Socio, Entrenador, Disciplina, Categoria, Fichaje, ParametroEvaluacion, PlanillaExamen, ResultadoExamen, MetricaRegistrada

class CicloTable(tables.Table):
# Opcional: puedes personalizar columnas específicas si quieres que tengan diseño (como el badge de activo)
    activo = tables.BooleanColumn(verbose_name='Estado')
    class Meta:
        model = Ciclo
        template_name = "django_tables2/bootstrap5.html"
        # Los campos que quieres mostrar
        fields = ("nombre", "fecha_inicio", "fecha_fin")
        attrs = {
            "class": "table table-hover table-bordered align-middle",
            "thead": {"class": "table-light"}
            }