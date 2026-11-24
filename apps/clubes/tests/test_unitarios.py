from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.clubes.forms import DisciplinaForm
from apps.clubes.models import Disciplina


class DisciplinaModelUnitTest(TestCase):
    """Pruebas unitarias aisladas sobre el modelo Disciplina."""

    def test_str_devuelve_nombre_disciplina(self):
        disciplina = Disciplina(
            nombre='Atletismo',
            descripcion='Pruebas de pista y campo'
        )
        self.assertEqual(str(disciplina), 'Atletismo')

    def test_nombre_supera_max_length_falla_validacion(self):
        # full_clean() ejecuta las validaciones de campo del modelo sin guardar en BD
        disciplina = Disciplina(
            nombre='A' * 101,
            descripcion='Descripción válida'
        )
        with self.assertRaises(ValidationError) as contexto:
            disciplina.full_clean()

        self.assertIn('nombre', contexto.exception.message_dict)

    def test_campos_obligatorios_vacios_fallan_full_clean(self):
        disciplina = Disciplina(nombre='', descripcion='')
        with self.assertRaises(ValidationError) as contexto:
            disciplina.full_clean()

        errores = contexto.exception.message_dict
        self.assertIn('nombre', errores)
        self.assertIn('descripcion', errores)


class DisciplinaFormUnitTest(TestCase):
    """Pruebas unitarias aisladas sobre las reglas de entrada de DisciplinaForm."""

    def test_form_valido_con_datos_completos(self):
        form = DisciplinaForm(data={
            'nombre': 'Vóley',
            'descripcion': 'Deporte en equipo con red'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalido_si_falta_descripcion(self):
        form = DisciplinaForm(data={
            'nombre': 'Vóley',
            'descripcion': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('descripcion', form.errors)