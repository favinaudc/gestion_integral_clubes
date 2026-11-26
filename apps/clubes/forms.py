import calendar
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Row, Submit
from django import forms
from django.core.validators import RegexValidator

from apps.customauth.models import Perfil

from .models import (
    Categoria,
    Ciclo,
    Club,
    Disciplina,
    Entrenador,
    Fichaje,
    MetricaRegistrada,
    ParametroEvaluacion,
    PlanillaExamen,
    ResultadoExamen,
    Socio,
    Usuario,
)


class CicloForm(forms.ModelForm):
    año = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu ciclo correspondiente...'
        }) )

    class Meta:
        #aqui campos extra 
        model = Ciclo
        fields = ['año']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar el FormHelper
        self.helper = FormHelper()

        # Definir el Layout
        self.helper.layout = Layout(
            # Los 3 campos dentro de una misma Row divididos en 3 Columnas (col-md-4 cada una para repartir el espacio)
            Row(
                Column('año', css_class='form-group col-md-12 mb-3'),
                css_class='row'
            ),
            # Botón verde (btn-success), texto en mayúsculas (text-uppercase) y centrado (text-center en un contenedor o clase de Bootstrap)
            # Nota: Agregamos una capa o clases utilitarias de Bootstrap para centrar el botón de forma limpia.
            Row(
                Column(
                    Submit('submit', 'GUARDAR', css_class='btn btn-success text-uppercase '),
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
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
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
                    Submit('submit', 'guardar', css_class='btn btn-success text-uppercase '),
                    
                    css_class='col-md-6 mx-auto text-center mt-3'
                )
            )
        )               

class SocioForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        required=False,
        label='Vincular cuenta existente (opcional)',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    club = forms.ModelChoiceField(
        queryset=Club.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    es_deportista = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    es_tutor = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    apto_medico = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    tutor_responsable = forms.ModelChoiceField(
        queryset=Socio.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Socio
        fields = (
            'usuario',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'telefono',
            'direccion',
            'club',
            'es_deportista',
            'es_tutor',
            'apto_medico',
            'tutor_responsable',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            perfil = self.instance.perfil_club.perfil
            self.initial.setdefault('usuario', perfil.usuario_id)
            self.initial.setdefault('nombre', perfil.nombre)
            self.initial.setdefault('apellido', perfil.apellido)
            self.initial.setdefault('fecha_nacimiento', perfil.fecha_nacimiento)
            self.initial.setdefault('telefono', perfil.telefono)
            self.initial.setdefault('direccion', perfil.direccion)
            self.initial.setdefault('club', self.instance.perfil_club.club_id)

        club_id = self.data.get('club') if self.is_bound else self.initial.get('club')
        if club_id:
            self.fields['tutor_responsable'].queryset = Socio.objects.filter(
                perfil_club__club_id=club_id,
                es_tutor=True,
            ).exclude(pk=self.instance.pk)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-3'),
                Column('apellido', css_class='form-group col-md-4 mb-3'),
                Column('fecha_nacimiento', css_class='form-group col-md-4 mb-3'),
                css_class='row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-3'),
                Column('direccion', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column('usuario', css_class='form-group col-md-6 mb-3'),
                Column('club', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column('es_deportista', css_class='form-group col-md-6 mb-3'),
                Column('es_tutor', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column('apto_medico', css_class='form-group col-md-6 mb-3'),
                Column('tutor_responsable', css_class='form-group col-md-6 mb-3'),
                css_class='row'
            ),
            Row(
                Column(
                    Submit('submit', 'GUARDAR SOCIO', css_class='btn btn-success text-uppercase '),
                    css_class='col-md-6 mx-auto text-center mt-3'
                )
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        club = cleaned_data.get('club')
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
        tutor_responsable = cleaned_data.get('tutor_responsable')

        perfil = None
        if usuario:
            perfil = Perfil.objects.filter(usuario=usuario).first()
        elif self.instance.pk:
            perfil = self.instance.perfil_club.perfil

        if perfil and club:
            socios_existentes = Socio.objects.filter(
                perfil_club__perfil=perfil,
                perfil_club__club=club,
                perfil_club__grupo_rol__name='SOCIO',
            )
            if self.instance.pk:
                socios_existentes = socios_existentes.exclude(pk=self.instance.pk)
            if socios_existentes.exists():
                self.add_error(None, 'Este perfil ya está registrado como socio en el club seleccionado.')

        if fecha_nacimiento:
            hoy = date.today()
            edad = (
                hoy.year
                - fecha_nacimiento.year
                - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            )
            if edad < 18 and not tutor_responsable:
                self.add_error(
                    'tutor_responsable',
                    'Los socios menores de edad deben tener un tutor responsable.',
                )
            elif tutor_responsable and club and tutor_responsable.perfil_club.club_id != club.pk:
                self.add_error(
                    'tutor_responsable',
                    'El tutor responsable debe pertenecer al mismo club.',
                )

        return cleaned_data
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
    club = forms.ModelChoiceField(
            queryset=Club.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    experiencia = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad de años de experiencia del entrenador'
            }) )
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del entrenador'
        }) )
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido del entrenador'
        }) )
    class Meta: 
        model = Entrenador
        fields = ['usuario', 'club', 'experiencia', 'nombre', 'apellido']

    def save(self, commit=True):
        # Guardamos el entrenador primero
        entrenador = super().save(commit=False)
        if commit:
            entrenador.save()
            # Asignamos el único club seleccionado envolviéndolo en una lista []
            club_seleccionado = self.cleaned_data.get('club')
            if club_seleccionado:
                entrenador.club.set([club_seleccionado])
        return entrenador

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                 Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('apellido', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                    ),
                Row(
                    Column('usuario', css_class='form-group col-md-6 mb-3'),
                    Column('club', css_class='form-group col-md-6 mb-3'),
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


class CategoriaCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disciplinas_por_categoria = {}

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None,
    ):
        option = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex=subindex,
            attrs=attrs,
        )
        disciplina_ids = self.disciplinas_por_categoria.get(str(value), ())
        if disciplina_ids:
            option['attrs']['data-disciplinas'] = ' '.join(disciplina_ids)
        return option


class GestionCrearEntrenadorForm(forms.Form):
    cuit_cuil = forms.CharField(
        max_length=11,
        label='CUIL/CUIT',
        validators=[
            RegexValidator(
                regex=r'^[0-9]{11}$',
                message='Ingresá los 11 dígitos del CUIL/CUIT, sin guiones.',
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sin guiones',
        }),
    )
    email = forms.EmailField(
        required=False,
        label='Correo electrónico de acceso',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    dni = forms.CharField(
        max_length=8,
        required=False,
        label='DNI',
        validators=[
            RegexValidator(
                regex=r'^[0-9]{7,8}$',
                message='Ingresá un DNI de 7 u 8 dígitos.',
            )
        ],
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Se usará como contraseña inicial para una cuenta nueva.',
    )
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    apellido = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
    )
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    experiencia = forms.IntegerField(
        required=False,
        min_value=0,
        label='Años de experiencia',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    disciplinas = forms.ModelMultipleChoiceField(
        queryset=Disciplina.objects.none(),
        label='Disciplinas',
        help_text='Podés seleccionar más de una disciplina.',
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'},
        ),
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.none(),
        label='Categorías',
        help_text='Seleccioná las categorías que dictará en las disciplinas elegidas.',
        widget=CategoriaCheckboxSelectMultiple(
            attrs={'class': 'form-check-input'},
        ),
    )

    def __init__(self, *args, club=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.club = club
        if club is not None:
            self.fields['disciplinas'].queryset = club.disciplinas.order_by(
                'nombre'
            )
            categorias = list(
                Categoria.objects.filter(club=club)
                .prefetch_related('disciplina')
                .order_by('nombre')
            )
            if self.is_bound:
                disciplina_ids = set(self.data.getlist('disciplinas'))
                if disciplina_ids:
                    categorias = [
                        categoria
                        for categoria in categorias
                        if disciplina_ids.intersection(
                            str(disciplina.pk)
                            for disciplina in categoria.disciplina.all()
                        )
                    ]
            self.fields['categorias'].queryset = Categoria.objects.filter(
                pk__in=[categoria.pk for categoria in categorias]
            ).order_by('nombre')
            self.fields[
                'categorias'
            ].widget.disciplinas_por_categoria = {
                str(categoria.pk): [
                    str(disciplina.pk)
                    for disciplina in categoria.disciplina.all()
                ]
                for categoria in categorias
            }

    def clean(self):
        cleaned_data = super().clean()
        cuit_cuil = cleaned_data.get('cuit_cuil')
        disciplinas = cleaned_data.get('disciplinas')
        categorias = cleaned_data.get('categorias')
        self.usuario_existente = None

        if cuit_cuil:
            self.usuario_existente = Usuario.objects.filter(
                cuit_cuil=cuit_cuil
            ).first()

        entrenador_existente = (
            Entrenador.objects.filter(usuario=self.usuario_existente).first()
            if self.usuario_existente
            else None
        )
        if not entrenador_existente:
            for campo in ('experiencia',):
                if cleaned_data.get(campo) is None:
                    self.add_error(campo, 'Este campo es obligatorio.')

        if self.usuario_existente is None:
            for campo in ('email', 'dni', 'nombre', 'apellido'):
                if not cleaned_data.get(campo):
                    self.add_error(campo, 'Este campo es obligatorio para una cuenta nueva.')

            email = cleaned_data.get('email')
            if email and Usuario.objects.filter(email__iexact=email).exists():
                self.add_error(
                    'email',
                    'Este correo ya está asociado a otra cuenta.',
                )

        if disciplinas and categorias:
            asignaciones = [
                (disciplina, categoria)
                for disciplina in disciplinas
                for categoria in categorias
                if categoria.disciplina.filter(pk=disciplina.pk).exists()
            ]
            if not asignaciones:
                self.add_error(
                    'categorias',
                    'Elegí categorías asociadas a las disciplinas seleccionadas.',
                )
            cleaned_data['asignaciones'] = asignaciones

        return cleaned_data

class DisciplinaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el nombre de la disciplina'
        }) )
        
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ingrese la descripción de la disciplina'
        }) )

    class Meta: 
        model = Disciplina
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 1, 'cols' : 1}),   
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('nombre', css_class='form-group col-md-4 mb-3'),                   
                    css_class='row'
                ),
                Row(
                    Column('descripcion', css_class='form-group col-md-12 mb-3'),
                    
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
        required=False,
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
    club = forms.ModelChoiceField(
        label = "Club",
        queryset=Club.objects.all(), widget=forms.Select(attrs={
            'class': 'form-control'
            }))
    disciplina = forms.ModelMultipleChoiceField(
        label = "Disciplina",
        queryset=Disciplina.objects.all(), widget=forms.SelectMultiple(attrs={
            'class': 'form-control'
            }))
    class Meta: 
        model = Categoria
        fields = ['nombre', 'descripcion', 'edad_minima', 'edad_maxima', 'club', 'disciplina']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('nombre', css_class='form-group col-md-4 mb-3'),
                    Column('edad_minima', css_class='form-group col-md-4 mb-3'),
                    Column('edad_maxima', css_class='form-group col-md-4 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('club', css_class='form-group col-md-6 mb-3'),
                    Column('disciplina', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('descripcion', css_class='form-group col-md-12 mb-3'),
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR CATEGORÍA', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )


class GestionCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'edad_minima', 'edad_maxima']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción (opcional)',
                'rows': 2,
            }),
            'edad_minima': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'edad_maxima': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }


class ReutilizarCategoriaForm(forms.Form):
    class CategoriaChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return f'{obj.nombre} ({obj.edad_minima}-{obj.edad_maxima})'

    categoria = CategoriaChoiceField(
        label='Categoría existente del club',
        queryset=Categoria.objects.none(),
        empty_label='Elegí una categoría',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, club, disciplina, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = (
            Categoria.objects.filter(club=club)
            .exclude(disciplina=disciplina)
            .order_by('nombre')
        )


def _fecha_limite_mayoria_edad():
    hoy = date.today()
    anio_limite = hoy.year - 18
    dia_limite = min(hoy.day, calendar.monthrange(anio_limite, hoy.month)[1])
    return date(anio_limite, hoy.month, dia_limite)


class SocioMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, socio):
        perfil = socio.perfil_club.perfil
        etiqueta = f'{perfil} (DNI: {perfil.dni or "sin registrar"})'
        if socio.tutor_responsable_id:
            etiqueta += f' | Responsable actual: {socio.tutor_responsable}'
        return etiqueta


class GestionCrearSocioForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='Correo electrónico de contacto',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el correo electrónico'
        })
    )

    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del socio'
        })
    )

    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido del socio'
        })
    )

    dni = forms.CharField(
        max_length=8,
        label='DNI',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el DNI'
        })
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date'
        })
    )

    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el teléfono del socio'
        })
    )

    direccion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la dirección del socio'
        })
    )

    tutor_responsable = forms.ModelChoiceField(
        queryset=Socio.objects.none(),
        required=False,
        label='Tutor responsable de este socio',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    es_tutor = forms.BooleanField(
        required=False,
        label='Este socio será tutor de otros socios',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    socios_a_cargo = SocioMultipleChoiceField(
        queryset=Socio.objects.none(),
        required=False,
        label='Socios menores a cargo',
        help_text=(
            'Los socios seleccionados quedarán a cargo de este tutor. '
            'Si ya tenían tutor, se reemplazará.'
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    apto_medico = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        help_text="@Suba el archivo del apto médico"
    )

    def __init__(self, *args, club_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if club_id:
            socios_del_club = Socio.objects.filter(
                perfil_club__club_id=club_id,
            ).select_related(
                'perfil_club__perfil',
                'tutor_responsable__perfil_club__perfil',
            )
            self.fields['tutor_responsable'].queryset = socios_del_club.filter(
                perfil_club__perfil__fecha_nacimiento__lte=_fecha_limite_mayoria_edad(),
            )
            self.fields['socios_a_cargo'].queryset = socios_del_club.filter(
                perfil_club__perfil__fecha_nacimiento__gt=_fecha_limite_mayoria_edad(),
            )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class="form-group col-md-4 mb-3"),
                Column('apellido', css_class="form-group col-md-4 mb-3"),
                Column('dni', css_class="form-group col-md-4 mb-3"),
            ),
            Row(
                Column('fecha_nacimiento', css_class="form-group col-md-4 mb-3"),
                Column('telefono', css_class="form-group col-md-4 mb-3"),
                Column('direccion', css_class="form-group col-md-4 mb-3"),
            ),
            Row(
                Column('email', css_class="form-group col-md-6 mb-3"),
                Column('apto_medico', css_class="form-group col-md-6 mb-3"),
            ),
            HTML('<h6 id="seccion-tutores-titulo" class="form-label text-uppercase">Responsabilidad de tutor</h6>'),
            HTML('<hr><section aria-labelledby="seccion-tutores-titulo">'),
            HTML('<div id="seccion-tutor-responsable" hidden>'),
            Row(
                Column('tutor_responsable', css_class="form-group col-md-12 mb-3"),
            ),
            HTML('</div>'),
            HTML('<div id="seccion-checkbox-es-tutor">'),
            Row(
                Column('es_tutor', css_class="form-group col-md-12 mb-3"),
            ),
            HTML('</div>'),
            HTML('<div id="seccion-socios-a-cargo" class="border rounded p-3 mb-3" hidden>'),
            HTML(
                '<label for="buscar-socios-a-cargo" class="form-label">'
                'Buscar socios menores</label>'
                '<input id="buscar-socios-a-cargo" type="search" '
                'class="form-control mb-3" placeholder="Buscar por nombre o DNI">'
            ),
            Row(
                Column('socios_a_cargo', css_class="form-group col-md-12 mb-3"),
            ),
            HTML('</div></section>'),
            Row(
                Column(
                    Submit('submit', 'GUARDAR SOCIO', css_class='btn btn-success text-uppercase '),
                    css_class='col-md-6 mx-auto text-center mt-3'
                )
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        es_tutor = cleaned_data.get('es_tutor', False)
        socios_a_cargo = cleaned_data.get('socios_a_cargo')
        tutor_responsable = cleaned_data.get('tutor_responsable')
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')

        if socios_a_cargo and not es_tutor:
            self.add_error(
                'socios_a_cargo',
                'Marca que este socio será tutor para asignarle socios menores.',
            )

        if fecha_nacimiento:
            hoy = date.today()
            edad = (
                hoy.year
                - fecha_nacimiento.year
                - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            )
            if edad < 18 and not tutor_responsable:
                self.add_error(
                    'tutor_responsable',
                    'Los socios menores de edad deben tener un tutor responsable.',
                )
            elif edad >= 18 and tutor_responsable:
                self.add_error(
                    'tutor_responsable',
                    'Solo los socios menores de edad deben tener tutor responsable.',
                )
            if edad < 18 and es_tutor:
                self.add_error(
                    'es_tutor',
                    'Solo un socio mayor de edad puede ser tutor.',
                )

        return cleaned_data

class FichajeForm(forms.ModelForm):
    socio = forms.ModelChoiceField(
            queryset=Socio.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    disciplina = forms.ModelChoiceField(
            queryset=Disciplina.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    categoria = forms.ModelChoiceField(
            queryset=Categoria.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    fecha_fichaje = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
                }))
    ciclo = forms.ModelChoiceField(
            queryset=Ciclo.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    class Meta: 
        model = Fichaje
        fields = ['socio', 'disciplina', 'categoria', 'fecha_fichaje', 'ciclo']   
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('socio', css_class='form-group col-md-6 mb-3'),
                    Column('disciplina', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('categoria', css_class='form-group col-md-6 mb-3'),
                    Column('fecha_fichaje', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('is_active', css_class='form-group col-md-6 mb-3'),
                    Column('ciclo', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        Submit('submit', 'GUARDAR FICHAJE', css_class='btn btn-success text-uppercase '),
                        css_class='col-md-6 mx-auto text-center mt-3'
                    )
                )
            )
    
    def clean(self):
        cleaned_data = super().clean()
        socio = cleaned_data.get('socio')
        disciplina = cleaned_data.get('disciplina')
        categoria = cleaned_data.get('categoria')

        if not (socio and disciplina and categoria):
            return cleaned_data

        club = socio.perfil_club.club
        if not club.disciplinas.filter(pk=disciplina.pk).exists():
            self.add_error(
                'disciplina',
                'El club del socio no está suscripto a esta disciplina.',
            )
        if categoria.club_id != club.pk:
            self.add_error(
                'categoria',
                'La categoría no pertenece al club del socio.',
            )
        elif not categoria.disciplina.filter(pk=disciplina.pk).exists():
            self.add_error(
                'categoria',
                'La categoría no está asociada a esta disciplina.',
            )

        return cleaned_data

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
    fichaje = forms.ModelChoiceField(
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
    diciplina = forms.ModelChoiceField(
            queryset=Disciplina.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    parametro = forms.ModelChoiceField(
            queryset=ParametroEvaluacion.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    class Meta: 
        model = PlanillaExamen
        fields = ['fichaje', 'fecha_examen', 'nombre', 'diciplina', 'parametro']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('fichaje', css_class='form-group col-md-6 mb-3'),
                    Column('fecha_examen', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('diciplina', css_class='form-group col-md-6 mb-3'),
                    css_class='row'
                ),
                Row(
                    Column('parametro', css_class='form-group col-md-6 mb-3'),
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
    planilla = forms.ModelChoiceField(
            queryset=PlanillaExamen.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    parametro = forms.ModelChoiceField(
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
        fields = ['planilla', 'parametro', 'resultado', 'observaciones']
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('planilla', css_class='form-group col-md-6 mb-3'),
                    Column('parametro', css_class='form-group col-md-6 mb-3'),
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
    resultado = forms.ModelChoiceField(
            queryset=ResultadoExamen.objects.all(), widget=forms.Select(attrs={
                'class': 'form-control'
                }))
    parametro = forms.ModelChoiceField(
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
        fields = ['resultado', 'parametro', 'valor_entero', 'valor_decimal', 'valor_tiempo', 'observaciones'] 
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Row(
                    Column('resultado', css_class='form-group col-md-6 mb-3'),
                    Column('parametro', css_class='form-group col-md-6 mb-3'),
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


