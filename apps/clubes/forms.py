from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Ciclo,Club,Socio,Usuario,Entrenador,Disciplina,Categoria,Fichaje,ParametroEvaluacion,PlanillaExamen,ResultadoExamen,MetricaRegistrada


class CicloForm(forms.ModelForm):
    año = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu ciclo correspondiente...'
        }) )
    fecha_inicio = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                
            }) )
    fecha_fin = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                
            }) )
    class Meta:
        #aqui campos extra 
        model = Ciclo
        fields = ['año', 'fecha_inicio', 'fecha_fin']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar el FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Definir el Layout
        self.helper.layout = Layout(
            # Los 3 campos dentro de una misma Row divididos en 3 Columnas (col-md-4 cada una para repartir el espacio)
            Row(
                Column('año', css_class='form-group col-md-4 mb-3'),
                Column('fecha_inicio', css_class='form-group col-md-4 mb-3'),
                Column('fecha_fin', css_class='form-group col-md-4 mb-3'),
                css_class='row'
            ),
            # Botón verde (btn-success), texto en mayúsculas (text-uppercase) y centrado (text-center en un contenedor o clase de Bootstrap)
            # Nota: Agregamos una capa o clases utilitarias de Bootstrap para centrar el botón de forma limpia.
            Row(
                Column(
                    Submit('submit', 'GUARDAR CICLO', css_class='btn btn-success text-uppercase '),
                    css_class='col-md-6 mx-auto text-center mt-3' # 'mx-auto' centra la columna y 'w-100' hace que ocupe el ancho de esa columna central
                )
            )
        )

class ClubForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del club'
        }) )
    direccion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la dirección del club'
        }) )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el teléfono del club'
        }) )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el correo electrónico del club'
        }) )
    fecha_fundacion = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control', 
            'type': 'date'
        }) )

    class Meta:
        model = Club
        fields = ['nombre', 'direccion', 'telefono', 'email', 'fecha_fundacion'] 

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        # Inicializar el FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'
        # Definir el Layout
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6 mb-3'),
                Column('direccion', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-4 mb-3'),
                Column('email', css_class='form-group col-md-4 mb-3'),
                Column('fecha_fundacion', css_class='form-group col-md-4 mb-3'),
                css_class='row'
            ),
            Row(
                Column(
                    Submit('submit', 'GUARDAR CLUB', css_class='btn btn-success text-uppercase '),
                    
                    css_class='col-md-6 mx-auto text-center mt-3'
                )
            )
        )               

class SocioForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
            queryset=Usuario.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    fecha_nacimiento = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                }))
    club_id = forms.ModelMultipleChoiceField(
            queryset=Club.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    es_deportista = forms.BooleanField(
            required=False, widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input'
                }))
    es_tutor = forms.BooleanField(
            required=False, widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input'
                }))
    apto_medico = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
            }))
    tutor_responsable_id = forms.ModelChoiceField(queryset=Socio.objects.all(), required=False, widget=forms.Select(attrs={
            'class': 'form-control'
            }))
    class Meta: 
        model = Socio
        fields = ['usuario', 'fecha_nacimiento', 'club_id', 'es_deportista', 'es_tutor', 'apto_medico', 'tutor_responsable_id']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('usuario', css_class='form-group col-md-6 mb-3'),
                    Column('fecha_nacimiento', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('club_id', css_class='form-group col-md-6 mb-3'),
                    Column('es_deportista', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('es_tutor', css_class='form-group col-md-6 mb-3'),
                    Column('apto_medico', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('tutor_responsable_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR SOCIO', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )        
class UsuarioForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del usuario'
        }) )
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido del usuario'
        }) )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el correo electrónico del usuario'
        }) )
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email'] 

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        # Inicializar el FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'
        # Definir el Layout
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6 mb-3'),
                Column('apellido', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column(
                    Submit('submit', 'GUARDAR USUARIO', css_class='btn btn-success text-uppercase '),
                    css_class='col-md-6 mx-auto text-center mt-3'
                )
            )
        )

class EntrenadorForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
            queryset=Usuario.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    club_id = forms.ModelMultipleChoiceField(
            queryset=Club.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    experiencia = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad de años de experiencia del entrenador'
            }) )
    class Meta: 
        model = Entrenador
        fields = ['usuario', 'club_id', 'experiencia']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('usuario', css_class='form-group col-md-6 mb-3'),
                    Column('club_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('experiencia', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR ENTRENADOR', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )

class DisciplinaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre de la disciplina'
        }) )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la descripción de la disciplina'
        }) )
    club_id = forms.ModelMultipleChoiceField(
            queryset=Club.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    entrenador_id = forms.ModelMultipleChoiceField(
            queryset=Entrenador.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    class Meta: 
        model = Disciplina
        fields = ['nombre', 'descripcion', 'club_id', 'entrenador_id']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('descripcion', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('club_id', css_class='form-group col-md-6 mb-3'),
                    Column('entrenador_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR DISCIPLINA', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )

class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre de la categoría'
        }) )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la descripción de la categoría'
        }) )
    edad_minima = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la edad mínima de la categoría'
            }) )
    edad_maxima = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la edad máxima de la categoría'
            }) )
    club_id = forms.ModelMultipleChoiceField(
            queryset=Club.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    disciplina_id = forms.ModelMultipleChoiceField(
            queryset=Disciplina.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    class Meta: 
        model = Categoria
        fields = ['nombre', 'descripcion', 'edad_minima', 'edad_maxima', 'club_id', 'disciplina_id']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('descripcion', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('edad_minima', css_class='form-group col-md-6 mb-3'),
                    Column('edad_maxima', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('club_id', css_class='form-group col-md-6 mb-3'),
                    Column('disciplina_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR CATEGORÍA', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
class FichajeForm(forms.ModelForm):
    socio_id = forms.ModelChoiceField(
            queryset=Socio.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    disciplina_id = forms.ModelChoiceField(
            queryset=Disciplina.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    categoria_id = forms.ModelChoiceField(
            queryset=Categoria.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    fecha_fichaje = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                }))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
            }))
    ciclo_id = forms.ModelChoiceField(
            queryset=Ciclo.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    class Meta: 
        model = Fichaje
        fields = ['socio_id', 'disciplina_id', 'categoria_id', 'fecha_fichaje', 'is_active', 'ciclo_id']   
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('socio_id', css_class='form-group col-md-6 mb-3'),
                    Column('disciplina_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('categoria_id', css_class='form-group col-md-6 mb-3'),
                    Column('fecha_fichaje', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('is_active', css_class='form-group col-md-6 mb-3'),
                    Column('ciclo_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR FICHAJE', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
class ParametroEvaluacionForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del parámetro de evaluación'
        }) )
    unidad_medida = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la unidad de medida del parámetro de evaluación'
        }) )
    tipo_dato = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el tipo de dato del parámetro de evaluación'
        }) )
    class Meta: 
        model = ParametroEvaluacion
        fields = ['nombre', 'unidad_medida', 'tipo_dato']   
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('unidad_medida', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('tipo_dato', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR PARÁMETRO DE EVALUACIÓN', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
class PlanillaExamenForm(forms.ModelForm):
    fichaje_id = forms.ModelChoiceField(
            queryset=Fichaje.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    fecha_examen = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                }))
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del examen'
        }) )
    diciplina_id = forms.ModelChoiceField(
            queryset=Disciplina.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    parametro_id = forms.ModelMultipleChoiceField(
            queryset=ParametroEvaluacion.objects.all(), widget=forms.SelectMultiple(attrs={
                'class': 'form-control'
                }))
    class Meta: 
        model = PlanillaExamen
        fields = ['fichaje_id', 'fecha_examen', 'nombre', 'diciplina_id', 'parametro_id']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('fichaje_id', css_class='form-group col-md-6 mb-3'),
                    Column('fecha_examen', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('diciplina_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('parametro_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR PLANILLA DE EXAMEN', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
class ResultadoExamenForm(forms.ModelForm):
    planilla_id = forms.ModelChoiceField(
            queryset=PlanillaExamen.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    parametro_id = forms.ModelChoiceField(
            queryset=ParametroEvaluacion.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    resultado = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el resultado del examen'
        }) )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese las observaciones del examen'
        }) )
    class Meta: 
        model = ResultadoExamen
        fields = ['planilla_id', 'parametro_id', 'resultado', 'observaciones']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('planilla_id', css_class='form-group col-md-6 mb-3'),
                    Column('parametro_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('resultado', css_class='form-group col-md-6 mb-3'),
                    Column('observaciones', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR RESULTADO DE EXAMEN', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
class MetricaRegistradaForm(forms.ModelForm):
    resultado_id = forms.ModelChoiceField(
            queryset=ResultadoExamen.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    parametro_id = forms.ModelChoiceField(
            queryset=ParametroEvaluacion.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    valor_entero = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el valor entero de la métrica registrada'
            }))
    valor_decimal = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el valor decimal de la métrica registrada'
            }))
    valor_tiempo = forms.DurationField(required=False, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el valor de tiempo de la métrica registrada (HH:MM:SS)'
            }))
    observaciones = forms.CharField(required=False, widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese las observaciones de la métrica registrada'
            }))
    class Meta: 
        model = MetricaRegistrada
        fields = ['resultado_id', 'parametro_id', 'valor_entero', 'valor_decimal', 'valor_tiempo', 'observaciones'] 
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('resultado_id', css_class='form-group col-md-6 mb-3'),
                    Column('parametro_id', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('valor_entero', css_class='form-group col-md-4 mb-3'),
                    Column('valor_decimal', css_class='form-group col-md-4 mb-3'),
                    Column('valor_tiempo', css_class='form-group col-md-4 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('observaciones', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR MÉTRICA REGISTRADA', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
