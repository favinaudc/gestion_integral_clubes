from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.clubes.models import Disciplina

User = get_user_model()


class DisciplinaTemplatesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            cuit_cuil='admin_test',
            password='password123'
        )
        self.client.login(cuit_cuil='admin_test', password='password123')

        self.futbol = Disciplina.objects.create(
            nombre='Fútbol',
            descripcion='Primera línea\nSegunda línea'
        )

        self.url_list = reverse('clubes:listar_disciplinas')
        self.url_create = reverse('clubes:crear_disciplina')
        self.url_detail = reverse('clubes:detalles_disciplina', kwargs={'pk': self.futbol.pk})
        self.url_update = reverse('clubes:editar_disciplina', kwargs={'pk': self.futbol.pk})
        self.url_delete = reverse('clubes:eliminar_disciplina', kwargs={'pk': self.futbol.pk})

    # ------------------------------------------------------------------
    # TEMPLATE: disciplina_list.html
    # ------------------------------------------------------------------
    def test_list_template_renderiza_tarjetas_y_acciones(self):
        response = self.client.get(self.url_list)

        # Herencia y tarjeta de acción superior
        self.assertTemplateUsed(response, 'base_apps.html')
        self.assertTemplateUsed(response, 'includes/action_card.html')
        self.assertContains(response, self.url_create)
        self.assertContains(response, 'Crear Disciplina')

        # Datos de la disciplina en la tarjeta
        self.assertContains(response, 'Fútbol')
        self.assertContains(response, 'Primera línea')

        # Enlace de editar y modal de eliminación específico por PK
        self.assertContains(response, f'href="{self.url_update}"')
        self.assertContains(response, f'data-bs-target="#modalEliminar{self.futbol.pk}"')
        self.assertContains(response, f'id="modalEliminar{self.futbol.pk}"')
        self.assertContains(response, f'action="{self.url_delete}"')

        # Sin filtro 'q', NO debe mostrarse el botón de limpiar filtros
        self.assertNotContains(response, 'title="Limpiar filtros"')

    def test_list_template_con_busqueda_activa(self):
        response = self.client.get(self.url_list, {'q': 'Fútbol'})

        # Mantiene el valor en el input y muestra el botón de limpiar
        self.assertContains(response, 'value="Fútbol"')
        self.assertContains(response, 'title="Limpiar filtros"')

    def test_list_template_estado_vacio_sin_busqueda(self):
        Disciplina.objects.all().delete()
        response = self.client.get(self.url_list)

        self.assertContains(response, 'id="mensajeVacio"')
        self.assertContains(response, 'No hay disciplinas registradas')
        self.assertNotContains(response, 'id="contenedorTarjetas"')

    def test_list_template_estado_vacio_sin_coincidencias(self):
        response = self.client.get(self.url_list, {'q': 'DeporteInexistenteXYZ'})

        self.assertContains(response, 'id="mensajeVacio"')
        self.assertContains(response, 'No hay coincidencias')
        self.assertNotContains(response, 'No hay disciplinas registradas')

    # ------------------------------------------------------------------
    # TEMPLATE: disciplina_detail.html
    # ------------------------------------------------------------------
    def test_detail_template_renderiza_filtros_y_boton_volver(self):
        response = self.client.get(self.url_detail)

        self.assertTemplateUsed(response, 'includes/boton_volver.html')

        # Filtro |upper en el encabezado
        self.assertContains(response, 'FÚTBOL')

        # Filtro |linebreaksbr convierte \n en <br>
        self.assertContains(response, 'Primera línea<br>Segunda línea', html=True)

        # Botón volver apuntando al listado
        self.assertContains(response, self.url_list)

    # ------------------------------------------------------------------
    # TEMPLATE: form_template.html (Create y Update)
    # ------------------------------------------------------------------
    def test_form_template_create_renderiza_titulo_y_crispy_form(self):
        response = self.client.get(self.url_create)

        self.assertTemplateUsed(response, 'base_apps.html')
        self.assertTemplateUsed(response, 'includes/boton_volver.html')

        # {{ titulo|upper }}
        self.assertContains(response, 'CREAR DISCIPLINA')

        # Campos del formulario renderizados por {% crispy form %}
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'name="nombre"')
        self.assertContains(response, 'name="descripcion"')
        self.assertContains(response, self.url_list)

    def test_form_template_update_renderiza_titulo_y_valores_precargados(self):
        response = self.client.get(self.url_update)

        self.assertContains(response, 'EDITAR DISCIPLINA')
        self.assertContains(response, 'value="Fútbol"')
        self.assertContains(response, 'Primera línea')

