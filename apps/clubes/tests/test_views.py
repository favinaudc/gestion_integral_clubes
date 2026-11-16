from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.clubes.models import Disciplina

User = get_user_model()


class DisciplinaViewsTest(TestCase):

    def setUp(self):
        # 1. Creamos un usuario para atravesar LoginRequiredMixinConMensaje
        self.user = User.objects.create_user(
            cuit_cuil='admin_test',
            password='password123'
        )
        self.client.login(cuit_cuil='admin_test', password='password123')

        # 2. Creamos registros base de Disciplina
        self.futbol = Disciplina.objects.create(
            nombre='Fútbol',
            descripcion='Deporte colectivo con balón'
        )
        self.natacion = Disciplina.objects.create(
            nombre='Natación',
            descripcion='Deporte acuático en piscina'
        )

        # 3. URLs nombradas
        self.url_list = reverse('clubes:listar_disciplinas')
        self.url_create = reverse('clubes:crear_disciplina')
        self.url_detail = reverse('clubes:detalles_disciplina', kwargs={'pk': self.futbol.pk})
        self.url_update = reverse('clubes:editar_disciplina', kwargs={'pk': self.futbol.pk})
        self.url_delete = reverse('clubes:eliminar_disciplina', kwargs={'pk': self.futbol.pk})

    # ------------------------------------------------------------------
    # PRUEBAS DE SEGURIDAD / MIXINS (Usuario no autenticado)
    # ------------------------------------------------------------------
    def test_vistas_requieren_login(self):
        """Verifica que todas las vistas redirijan si no hay sesión iniciada."""
        self.client.logout()
        urls = [
            self.url_list,
            self.url_create,
            self.url_detail,
            self.url_update,
            self.url_delete,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # LIST VIEW (DisciplinaListView)
    # ------------------------------------------------------------------
    def test_list_view_sin_filtro(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubes/disciplina/disciplina_list.html')
        self.assertEqual(response.context['q'], '')
        self.assertQuerySetEqual(
            response.context['disciplinas'],
            [self.futbol, self.natacion],
            ordered=False
        )

    def test_list_view_con_filtro_busqueda(self):
        """Verifica el filtro Q por nombre o descripción y que 'q' vuelva en el contexto."""
        response = self.client.get(self.url_list, {'q': 'acuático'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['q'], 'acuático')
        self.assertIn(self.natacion, response.context['disciplinas'])
        self.assertNotIn(self.futbol, response.context['disciplinas'])

    # ------------------------------------------------------------------
    # DETAIL VIEW (DisciplinaDetailView)
    # ------------------------------------------------------------------
    def test_detail_view(self):
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubes/disciplina/disciplina_detail.html')
        self.assertEqual(response.context['disciplina'], self.futbol)
        self.assertEqual(response.context['url_volver'], 'clubes:listar_disciplinas')

    def test_detail_view_inexistente_devuelve_404(self):
        url_404 = reverse('clubes:detalles_disciplina', kwargs={'pk': 9999})
        response = self.client.get(url_404)
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------
    # CREATE VIEW (DisciplinaCreateView)
    # ------------------------------------------------------------------
    def test_create_view_get(self):
        response = self.client.get(self.url_create)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['titulo'], 'Crear disciplina')
        self.assertEqual(response.context['url_volver'], 'clubes:listar_disciplinas')

    def test_create_view_post_valido(self):
        datos = {
            'nombre': 'Básquetbol',
            'descripcion': 'Deporte de cancha con aro'
        }
        response = self.client.post(self.url_create, data=datos)

        # Verifica creación en BD
        self.assertEqual(Disciplina.objects.count(), 3)
        nueva_disciplina = Disciplina.objects.get(nombre='Básquetbol')

        # Verifica redirección al detalle usando get_success_url()
        url_esperada = reverse('clubes:detalles_disciplina', kwargs={'pk': nueva_disciplina.pk})
        self.assertRedirects(response, url_esperada)

    def test_create_view_post_invalido(self):
        """Si faltan campos obligatorios, no crea el objeto y vuelve a mostrar el form (200)."""
        response = self.client.post(self.url_create, data={'nombre': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Disciplina.objects.count(), 2)
        self.assertFormError(response.context['form'], 'nombre', 'Este campo es obligatorio.')

    # ------------------------------------------------------------------
    # UPDATE VIEW (DisciplinaUpdateView)
    # ------------------------------------------------------------------
    def test_update_view_get(self):
        response = self.client.get(self.url_update)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['titulo'], 'Editar disciplina')
        self.assertEqual(response.context['url_volver'], 'clubes:listar_disciplinas')

    def test_update_view_post_valido(self):
        datos_editados = {
            'nombre': 'Fútbol 11',
            'descripcion': 'Descripción actualizada'
        }
        response = self.client.post(self.url_update, data=datos_editados)

        self.assertRedirects(response, self.url_list)
        self.futbol.refresh_from_db()
        self.assertEqual(self.futbol.nombre, 'Fútbol 11')
        self.assertEqual(self.futbol.descripcion, 'Descripción actualizada')

