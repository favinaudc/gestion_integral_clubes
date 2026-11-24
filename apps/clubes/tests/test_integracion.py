from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from apps.clubes.forms import DisciplinaForm
from apps.clubes.models import Disciplina
from apps.clubes.views.disciplinas_views import (  # Ajustar ruta si están en views.py
    DisciplinaCreateView,
    DisciplinaListView,
)

User = get_user_model()


class DisciplinaFormModelIntegrationTest(TestCase):
    """Integración entre DisciplinaForm, el modelo Disciplina y la base de datos."""

    def test_form_save_crea_registro_en_bd(self):
        form = DisciplinaForm(data={
            'nombre': 'Handball',
            'descripcion': 'Deporte de cancha con balón'
        })
        self.assertTrue(form.is_valid())

        disciplina_guardada = form.save()

        self.assertIsNotNone(disciplina_guardada.pk)
        self.assertEqual(Disciplina.objects.count(), 1)
        self.assertEqual(
            Disciplina.objects.get(pk=disciplina_guardada.pk).nombre,
            'Handball'
        )

    def test_form_con_instance_actualiza_sin_duplicar(self):
        disciplina = Disciplina.objects.create(
            nombre='Rugby',
            descripcion='Descripción original'
        )
        form = DisciplinaForm(
            data={'nombre': 'Rugby Union', 'descripcion': 'Actualizada'},
            instance=disciplina
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Disciplina.objects.count(), 1)
        disciplina.refresh_from_db()
        self.assertEqual(disciplina.nombre, 'Rugby Union')


class DisciplinaViewsORMIntegrationTest(TestCase):
    """Integración entre la lógica interna de las vistas, mixins y el ORM usando RequestFactory."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            cuit_cuil='20123456789',
            password='password123'
        )
        self.futbol = Disciplina.objects.create(
            nombre='Fútbol',
            descripcion='Deporte colectivo con balón'
        )
        self.natacion = Disciplina.objects.create(
            nombre='Natación',
            descripcion='Deporte acuático en piscina'
        )

    def _preparar_request(self, request):
        """Adjunta usuario autenticado y soporte de mensajes (RequestFactory no ejecuta middlewares)."""
        request.user = self.user
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        return request

    def test_list_view_get_queryset_filtra_en_orm(self):
        request = self._preparar_request(
            self.factory.get('/disciplinas/', {'q': 'balón'})
        )
        vista = DisciplinaListView()
        vista.setup(request)

        queryset = vista.get_queryset()

        self.assertEqual(list(queryset), [self.futbol])

    def test_create_view_integra_form_orm_y_success_url(self):
        request = self._preparar_request(
            self.factory.post('/disciplinas/crear/', {
                'nombre': 'Hockey',
                'descripcion': 'Deporte sobre césped'
            })
        )
        response = DisciplinaCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Disciplina.objects.count(), 3)
        creada = Disciplina.objects.get(nombre='Hockey')
        self.assertIn(str(creada.pk), response.url)