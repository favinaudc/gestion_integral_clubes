import django_tables2 as tables
from .models import Club, Ciclo, Socio, Entrenador, Disciplina, Categoria, Fichaje, ParametroEvaluacion, PlanillaExamen, ResultadoExamen, MetricaRegistrada

class CicloTable(tables.Table):
# Opcional: puedes personalizar columnas específicas si quieres que tengan diseño (como el badge de activo)
    #activo = tables.BooleanColumn(verbose_name='Estado') solo es para devolver un booleano a mostrar en la tabla   
    activo = tables.TemplateColumn(
        template_code='''
            <span class="badge bg-{% if record.activo %}success{% else %}secondary{% endif %} rounded-pill">
                {% if record.activo %}Activo{% else %}Inactivo{% endif %}
            </span>
    ''',
    verbose_name='Estado'
    )
    acciones = tables.TemplateColumn(
        template_code='''
            <div class="text-center">
                <a href="{% url 'clubes:editar_ciclo' record.pk %}" class="btn btn-sm btn-outline-primary me-1">
                    <i class="fas fa-edit"></i> Editar
                </a>
                <a href="{% url 'clubes:eliminar_ciclo' record.pk %}" class="btn btn-sm btn-outline-danger">
                    <i class="fas fa-trash"></i> Eliminar
                </a>
            </div>
        ''',
        verbose_name='Acciones',
        orderable=False
    )  
#Uso de record: En django-tables2, la variable para referirte a la fila actual dentro de una columna de plantilla es record (en lugar de ciclo).
#orderable=False: Es recomendable desactivar el ordenamiento en la columna de acciones, ya que no tiene sentido ordenar la tabla basándose en los botones de editar o eliminar.
#template_code: Te permite escribir el HTML directamente en el archivo de la tabla sin necesidad de crear archivos HTML externos, ideal para componentes pequeños como este.
    class Meta:
        model = Ciclo
        template_name = "django_tables2/bootstrap5.html"
        # Los campos que quieres mostrar
        fields = ("año", "fecha_inicio", "fecha_fin","activo","acciones")
        attrs = {
            "class": "table table-hover table-bordered align-middle",
            "thead": {"class": "table-light"}
            }