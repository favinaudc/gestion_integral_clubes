from datetime import date

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views import View

from ..models import (
    AsignacionEntrenador,
    Categoria,
    Ciclo,
    CicloClub,
    Club,
    Disciplina,
    Entrenador,
    Socio,
)
from apps.clubes.forms import FichajeForm
from apps.customauth.models import Perfil, PerfilClub, Usuario
from apps.customauth.mixins import ValidarRolClubMixin


class ClubAdminProbeView(ValidarRolClubMixin, View):
    rol_requerido = ["CLUB_ADMIN"]

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200)


class SocioCreateViewTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            cuit_cuil="20123456789",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(self.user)
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        self.perfil = Perfil.objects.create(
            nombre="Ana",
            apellido="Prueba",
            fecha_nacimiento=date(1990, 1, 1),
        )

    def test_create_socio_without_usuario(self):
        create_url = reverse("clubes:crear_socio")# carga formulario
        response = self.client.get(create_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="nombre"')
        self.assertContains(response, 'name="fecha_nacimiento"')

        response = self.client.post(
            create_url,
            {
                "nombre": "Beatriz",
                "apellido": "Prueba",
                "fecha_nacimiento": "1990-01-01",
                "telefono": "",
                "direccion": "",
                "club": self.club.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("clubes:listar_socios"))

        socio = Socio.objects.get()
        self.assertIsNone(socio.perfil_club.perfil.usuario)
        self.assertEqual(socio.perfil_club.perfil.nombre, "Beatriz")
        self.assertEqual(socio.perfil_club.club, self.club)
        self.assertEqual(socio.perfil_club.grupo_rol.name, "SOCIO")
        self.assertIsNotNone(socio.pk)
        self.assertEqual(str(socio), "Beatriz Prueba")

    def test_profile_can_have_different_roles_in_different_clubs(self):
        grupo_socio, _ = Group.objects.get_or_create(name="SOCIO")
        grupo_admin_club, _ = Group.objects.get_or_create(name="CLUB_ADMIN")
        segundo_club = Club.objects.create(
            nombre="Segundo club",
            direccion="Avenida 456",
            telefono="987654321",
            email="segundo@example.com",
            fecha_fundacion=date(2005, 1, 1),
        )
        perfil = self.user.perfil
        perfil.nombre = "Usuario"
        perfil.apellido = "Con roles"
        perfil.fecha_nacimiento = date(1990, 1, 1)
        perfil.save()

        membresia_socio = PerfilClub.objects.create(
            perfil=perfil,
            club=self.club,
            grupo_rol=grupo_socio,
        )
        membresia_admin = PerfilClub.objects.create(
            perfil=perfil,
            club=segundo_club,
            grupo_rol=grupo_admin_club,
        )
        socio = Socio.objects.create(perfil_club=membresia_socio)

        self.assertEqual(socio.perfil_club.perfil, perfil)
        self.assertEqual(membresia_admin.perfil, perfil)
        self.assertEqual(membresia_socio.grupo_rol.name, "SOCIO")
        self.assertEqual(membresia_admin.grupo_rol.name, "CLUB_ADMIN")

    def test_club_permission_uses_the_role_for_that_club(self):
        grupo_admin_club, _ = Group.objects.get_or_create(name="CLUB_ADMIN")
        PerfilClub.objects.create(
            perfil=self.user.perfil,
            club=self.club,
            grupo_rol=grupo_admin_club,
        )
        request = RequestFactory().get("/")
        request.user = self.user

        response = ClubAdminProbeView.as_view()(request, pk=self.club.pk)

        self.assertEqual(response.status_code, 200)

    # Que la vista que lista a los socios muestre correctamente la información detallada, las etiquetas de estado (si es deportista,
    # si tiene apto médico vigente, si no tiene usuario) y las acciones de Editar y Eliminar agrupadas
    # correctamente sin duplicar cabeceras innecesarias.

    def test_socio_list_shows_details_and_combined_actions(self):
        grupo_socio, _ = Group.objects.get_or_create(name="SOCIO")
        self.perfil.dni = "30123456"
        self.perfil.save(update_fields=["dni"])
        membership = PerfilClub.objects.create(
            perfil=self.perfil,
            club=self.club,
            grupo_rol=grupo_socio,
        )
        socio = Socio.objects.create(
            perfil_club=membership,
            es_deportista=True,
        )
        response = self.client.get(reverse("clubes:listar_socios"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sin usuario")
        self.assertContains(response, "30123456")
        self.assertContains(response, self.club.nombre)
        self.assertContains(response, "Sí")
        self.assertContains(response, "No cargado")
        self.assertContains(response, reverse("clubes:editar_socio", args=[socio.pk]))
        self.assertContains(response, reverse("clubes:eliminar_socio", args=[socio.pk]))


class GestionCrearSocioTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            cuit_cuil="20123456789",
            email="admin@example.com",
            password="test-password",
        )
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        grupo_admin_club, _ = Group.objects.get_or_create(name="CLUB_ADMIN")
        self.user.groups.add(grupo_admin_club)
        self.user.grupo_activo = grupo_admin_club
        self.user.save(update_fields=["grupo_activo"])
        PerfilClub.objects.create(
            perfil=self.user.perfil,
            club=self.club,
            grupo_rol=grupo_admin_club,
        )
        permiso = Permission.objects.get(
            content_type__app_label="clubes",
            codename="gestionar_club",
        )
        self.user.user_permissions.add(permiso)
        self.client.force_login(self.user)
        self.url = reverse("clubes:gestion_crear_socio", args=[self.club.pk])
        self.form_data = {
            "nombre": "Beatriz",
            "apellido": "Prueba",
            "dni": "30123456",
            "email": "beatriz@example.com",
            "fecha_nacimiento": "1990-01-01",
            "telefono": "123456789",
            "direccion": "Calle 123",
        }

    def test_club_admin_creates_socio_without_user(self):
        response = self.client.post(self.url, self.form_data)

        self.assertRedirects(
            response,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )
        socio = Socio.objects.get()
        perfil = socio.perfil_club.perfil
        self.assertIsNone(perfil.usuario)
        self.assertEqual(perfil.dni, "30123456")
        self.assertEqual(perfil.email, "beatriz@example.com")
        self.assertEqual(socio.perfil_club.club, self.club)
        self.assertEqual(socio.perfil_club.grupo_rol.name, "SOCIO")

        listado = self.client.get(
            reverse("clubes:gestionar_club", args=[self.club.pk])
        )
        self.assertContains(listado, "Beatriz")
        self.assertContains(listado, "30123456")
        self.assertContains(
            listado,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )

    def test_tutor_can_be_assigned_multiple_minor_members(self):
        tutor_anterior = self.crear_socio(
            "Tutor",
            "Anterior",
            date(1980, 1, 1),
            "30000000",
            es_tutor=True,
        )
        menores = [
            self.crear_socio(
                f"Menor {indice}",
                "Prueba",
                date(2012, 1, indice),
                f"3000000{indice}",
                tutor_responsable=tutor_anterior,
            )
            for indice in (1, 2)
        ]
        formulario = self.client.get(self.url)
        self.assertContains(formulario, 'id="id_es_tutor"')
        self.assertContains(formulario, 'id="buscar-socios-a-cargo"')
        self.assertContains(formulario, f'value="{menores[0].pk}"')
        self.assertContains(formulario, f'value="{menores[1].pk}"')
        self.assertNotContains(formulario, 'name="cuit_cuil"')

        response = self.client.post(
            self.url,
            {
                **self.form_data,
                "es_tutor": "on",
                "socios_a_cargo": [menor.pk for menor in menores],
            },
        )

        self.assertRedirects(
            response,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )
        nuevo_tutor = Socio.objects.get(perfil_club__perfil__dni="30123456")
        self.assertTrue(nuevo_tutor.es_tutor)
        for menor in menores:
            menor.refresh_from_db()
            self.assertEqual(menor.tutor_responsable, nuevo_tutor)

    def test_minor_member_requires_an_existing_tutor(self):
        response = self.client.post(
            self.url,
            {
                **self.form_data,
                "fecha_nacimiento": "2015-04-04",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Socio.objects.count(), 0)
        self.assertIn(
            "Los socios menores de edad deben tener un tutor responsable.",
            response.context["form"].errors["tutor_responsable"],
        )

    def test_minor_member_can_select_an_existing_tutor(self):
        tutor = self.crear_socio(
            "Tutor",
            "Prueba",
            date(1980, 1, 1),
            "30000000",
        )
        formulario = self.client.get(self.url)
        self.assertContains(formulario, f'value="{tutor.pk}"')
        response = self.client.post(
            self.url,
            {
                **self.form_data,
                "fecha_nacimiento": "2015-04-04",
                "tutor_responsable": tutor.pk,
            },
        )

        self.assertRedirects(
            response,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )
        menor = Socio.objects.get(perfil_club__perfil__dni="30123456")
        self.assertEqual(menor.tutor_responsable, tutor)
        tutor.refresh_from_db()
        self.assertTrue(tutor.es_tutor)

    def crear_socio(
        self,
        nombre,
        apellido,
        fecha_nacimiento,
        dni,
        es_tutor=False,
        tutor_responsable=None,
    ):
        grupo_socio, _ = Group.objects.get_or_create(name="SOCIO")
        perfil = Perfil.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
        )
        perfil_club = PerfilClub.objects.create(
            perfil=perfil,
            club=self.club,
            grupo_rol=grupo_socio,
        )
        return Socio.objects.create(
            perfil_club=perfil_club,
            es_tutor=es_tutor,
            tutor_responsable=tutor_responsable,
        )


class GestionDisciplinasTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            cuit_cuil="20123456789",
            email="admin@example.com",
            password="test-password",
        )
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        grupo_club_admin, _ = Group.objects.get_or_create(name="CLUB_ADMIN")
        permiso = Permission.objects.get(
            content_type__app_label="clubes",
            codename="suscribir_club_a_disciplina",
        )
        grupo_club_admin.permissions.add(permiso)
        self.user.groups.add(grupo_club_admin)
        self.user.grupo_activo = grupo_club_admin
        self.user.save(update_fields=["grupo_activo"])
        PerfilClub.objects.create(
            perfil=self.user.perfil,
            club=self.club,
            grupo_rol=grupo_club_admin,
        )
        self.client.force_login(self.user)
        self.url = reverse("clubes:gestion_disciplinas", args=[self.club.pk])

    def test_lists_catalog_and_marks_subscription_status(self):
        suscripta_z = Disciplina.objects.create(
            nombre="Natacion",
            descripcion="Entrenamiento en pileta.",
        )
        suscripta_a = Disciplina.objects.create(
            nombre="Atletismo",
            descripcion="Carreras y saltos.",
        )
        disponible = Disciplina.objects.create(
            nombre="Basket",
            descripcion="Deporte de equipo.",
        )
        self.club.disciplinas.add(suscripta_z, suscripta_a)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, suscripta_z.nombre)
        self.assertContains(response, suscripta_a.nombre)
        self.assertContains(response, disponible.nombre)
        self.assertContains(response, "disciplina-card-suscripta")
        self.assertContains(response, "disciplina-card-no-suscripta")
        self.assertContains(response, "Desuscribirse")
        self.assertContains(response, "Suscribirse")
        self.assertEqual(
            response.context["disciplinas_suscriptas"],
            {suscripta_z.pk, suscripta_a.pk},
        )
        self.assertEqual(
            list(response.context["disciplinas"]),
            [suscripta_a, disponible, suscripta_z],
        )

        response_suscriptas = self.client.get(
            self.url,
            {"filtro": "suscriptas"},
        )
        self.assertEqual(
            list(response_suscriptas.context["disciplinas"]),
            [suscripta_a, suscripta_z],
        )

        response_no_suscriptas = self.client.get(
            self.url,
            {"filtro": "no_suscriptas"},
        )
        self.assertEqual(
            list(response_no_suscriptas.context["disciplinas"]),
            [disponible],
        )

    def test_club_admin_can_subscribe_and_unsubscribe(self):
        disciplina = Disciplina.objects.create(
            nombre="Hockey",
            descripcion="Deporte de equipo.",
        )

        response = self.client.post(
            self.url,
            {"accion": "suscribir", "disciplina_id": disciplina.pk},
        )
        self.assertRedirects(response, self.url)
        self.assertTrue(self.club.disciplinas.filter(pk=disciplina.pk).exists())

        response = self.client.post(
            self.url,
            {"accion": "desuscribir", "disciplina_id": disciplina.pk},
        )
        self.assertRedirects(response, self.url)
        self.assertFalse(self.club.disciplinas.filter(pk=disciplina.pk).exists())

    def test_user_without_subscription_permission_cannot_access(self):
        Group.objects.get(name="CLUB_ADMIN").permissions.clear()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)


class GestionCategoriasTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            cuit_cuil="20123456789",
            email="admin@example.com",
            password="test-password",
        )
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        self.otro_club = Club.objects.create(
            nombre="Otro club",
            direccion="Calle 456",
            telefono="123456789",
            email="otro@example.com",
            fecha_fundacion=date(2001, 1, 1),
        )
        grupo_club_admin, _ = Group.objects.get_or_create(name="CLUB_ADMIN")
        permiso = Permission.objects.get(
            content_type__app_label="clubes",
            codename="gestionar_club",
        )
        grupo_club_admin.permissions.add(permiso)
        self.user.groups.add(grupo_club_admin)
        self.user.grupo_activo = grupo_club_admin
        self.user.save(update_fields=["grupo_activo"])
        PerfilClub.objects.create(
            perfil=self.user.perfil,
            club=self.club,
            grupo_rol=grupo_club_admin,
        )
        self.disciplina_a = Disciplina.objects.create(
            nombre="Atletismo",
            descripcion="Carreras y saltos.",
        )
        self.disciplina_b = Disciplina.objects.create(
            nombre="Natacion",
            descripcion="Entrenamiento en pileta.",
        )
        self.no_suscripta = Disciplina.objects.create(
            nombre="Voley",
            descripcion="Deporte de equipo.",
        )
        self.club.disciplinas.add(self.disciplina_a, self.disciplina_b)
        self.client.force_login(self.user)
        self.url = reverse("clubes:gestion_categorias", args=[self.club.pk])

    def crear_categoria(self, club, nombre, disciplina):
        categoria = Categoria.objects.create(
            club=club,
            nombre=nombre,
            edad_minima=10,
            edad_maxima=12,
        )
        categoria.disciplina.add(disciplina)
        return categoria

    def test_lista_solo_disciplinas_suscriptas_en_orden_alfabetico(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["disciplinas"]),
            [self.disciplina_a, self.disciplina_b],
        )
        self.assertNotContains(response, self.no_suscripta.nombre)

    def test_crea_categoria_con_descripcion_opcional_y_rango_valido(self):
        response = self.client.post(
            self.url,
            {
                "accion": "crear",
                "disciplina_id": self.disciplina_a.pk,
                "nombre": "Sub 12",
                "edad_minima": "10",
                "edad_maxima": "12",
            },
        )

        categoria = Categoria.objects.get(nombre="Sub 12")
        self.assertRedirects(
            response,
            f"{self.url}?disciplina_id={self.disciplina_a.pk}#gestion-categoria",
        )
        self.assertEqual(categoria.club, self.club)
        self.assertEqual(categoria.descripcion, "")
        self.assertTrue(categoria.disciplina.filter(pk=self.disciplina_a.pk).exists())

    def test_rechaza_rango_de_edades_invalido(self):
        response = self.client.post(
            self.url,
            {
                "accion": "crear",
                "disciplina_id": self.disciplina_a.pk,
                "nombre": "Rango inválido",
                "edad_minima": "12",
                "edad_maxima": "12",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Categoria.objects.filter(nombre="Rango inválido").exists())
        self.assertIn(
            "La edad máxima debe ser mayor que la edad mínima.",
            response.context["form_categoria"].errors["edad_maxima"],
        )

    def test_reutiliza_categoria_del_club_y_no_la_duplica(self):
        categoria = self.crear_categoria(
            self.club,
            "Sub 12",
            self.disciplina_a,
        )
        categoria_otro_club = self.crear_categoria(
            self.otro_club,
            "Juveniles",
            self.disciplina_a,
        )

        response = self.client.post(
            self.url,
            {
                "accion": "reutilizar",
                "disciplina_id": self.disciplina_b.pk,
                "categoria": categoria.pk,
            },
        )

        self.assertRedirects(
            response,
            f"{self.url}?disciplina_id={self.disciplina_b.pk}#gestion-categoria",
        )
        self.assertTrue(categoria.disciplina.filter(pk=self.disciplina_b.pk).exists())
        self.assertFalse(
            categoria_otro_club.disciplina.filter(pk=self.disciplina_b.pk).exists()
        )
        self.assertEqual(Categoria.objects.count(), 2)

    def test_quitar_categoria_solo_desasocia_de_esa_disciplina(self):
        categoria = self.crear_categoria(
            self.club,
            "Sub 12",
            self.disciplina_a,
        )
        categoria.disciplina.add(self.disciplina_b)

        response = self.client.post(
            self.url,
            {
                "accion": "quitar",
                "disciplina_id": self.disciplina_a.pk,
                "categoria_id": categoria.pk,
            },
        )

        self.assertRedirects(
            response,
            f"{self.url}?disciplina_id={self.disciplina_a.pk}#gestion-categoria",
        )
        self.assertTrue(Categoria.objects.filter(pk=categoria.pk).exists())
        self.assertFalse(categoria.disciplina.filter(pk=self.disciplina_a.pk).exists())
        self.assertTrue(categoria.disciplina.filter(pk=self.disciplina_b.pk).exists())

    def test_no_permite_gestionar_una_disciplina_no_suscripta(self):
        response = self.client.get(
            self.url,
            {"disciplina_id": self.no_suscripta.pk},
        )

        self.assertEqual(response.status_code, 404)


class FichajeCategoriaValidationTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        self.otro_club = Club.objects.create(
            nombre="Otro club",
            direccion="Calle 456",
            telefono="123456789",
            email="otro@example.com",
            fecha_fundacion=date(2001, 1, 1),
        )
        self.disciplina = Disciplina.objects.create(
            nombre="Natacion",
            descripcion="Entrenamiento en pileta.",
        )
        self.club.disciplinas.add(self.disciplina)
        grupo_socio, _ = Group.objects.get_or_create(name="SOCIO")
        perfil = Perfil.objects.create(
            nombre="Socio",
            apellido="Prueba",
            fecha_nacimiento=date(2000, 1, 1),
        )
        perfil_club = PerfilClub.objects.create(
            perfil=perfil,
            club=self.club,
            grupo_rol=grupo_socio,
        )
        self.socio = Socio.objects.create(perfil_club=perfil_club)
        self.ciclo = Ciclo.objects.create(año=2026)
        self.categoria = Categoria.objects.create(
            club=self.club,
            nombre="Sub 18",
            edad_minima=13,
            edad_maxima=17,
        )
        self.categoria.disciplina.add(self.disciplina)

    def form_data(self, categoria):
        return {
            "socio": self.socio.pk,
            "disciplina": self.disciplina.pk,
            "categoria": categoria.pk,
            "fecha_fichaje": "2026-01-02",
            "ciclo": self.ciclo.pk,
        }

    def test_accepts_category_from_the_same_club_and_discipline(self):
        form = FichajeForm(data=self.form_data(self.categoria))

        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_category_from_another_club(self):
        categoria_otro_club = Categoria.objects.create(
            club=self.otro_club,
            nombre="Sub 18",
            edad_minima=13,
            edad_maxima=17,
        )
        categoria_otro_club.disciplina.add(self.disciplina)

        form = FichajeForm(data=self.form_data(categoria_otro_club))

        self.assertFalse(form.is_valid())
        self.assertIn("La categoría no pertenece al club del socio.", form.errors["categoria"])


# Pruebas de validación de fechas para CicloClub
class CicloClubDateValidationTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        self.ciclo = Ciclo.objects.create(año=2025)

    # Que si asignas fechas que están dentro del año del ciclo (por ejemplo,
    # desde el 1 de enero de 2025 hasta el 31 de diciembre de 2025

    def test_dates_in_cycle_year_can_be_saved(self):
        relacion = CicloClub.objects.create(
            club=self.club,
            ciclo=self.ciclo,
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 12, 31),
        )

        self.assertIsNotNone(relacion.pk)

    # si intentas registrar una fecha de inicio (fecha_inicio) que pertenece a un año diferente al del ciclo
    # (por ejemplo, poner el año 2024 en un ciclo del 2025). Además, verifica que el error esté específicamente
    # asociado al campo fecha_inicio
    def test_start_date_must_match_cycle_year(self):
        with self.assertRaises(ValidationError) as error:
            CicloClub.objects.create(
                club=self.club,
                ciclo=self.ciclo,
                fecha_inicio=date(2024, 12, 31),
                fecha_fin=date(2025, 12, 31),
            )

        self.assertIn("fecha_inicio", error.exception.message_dict)

    # Valida que si la fecha de cierre pertenece a un año posterior o distinto al del ciclo
    # (por ejemplo, año 2026), se rechace con un error de validación en dicho campo.
    def test_end_date_must_match_cycle_year(self):
        with self.assertRaises(ValidationError) as error:
            CicloClub.objects.create(
                club=self.club,
                ciclo=self.ciclo,
                fecha_inicio=date(2025, 1, 1),
                fecha_fin=date(2026, 1, 1),
            )

        self.assertIn("fecha_fin", error.exception.message_dict)


class GestionCrearEntrenadorTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            cuit_cuil="20123456789",
            email="admin@example.com",
            password="test-password",
        )
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )
        grupo_admin_club, _ = Group.objects.get_or_create(name="CLUB_ADMIN")
        PerfilClub.objects.create(
            perfil=self.user.perfil,
            club=self.club,
            grupo_rol=grupo_admin_club,
        )
        permiso = Permission.objects.get(
            content_type__app_label="clubes",
            codename="gestionar_club",
        )
        self.user.user_permissions.add(permiso)
        self.client.force_login(self.user)

        self.disciplina = Disciplina.objects.create(
            nombre="Natación",
            descripcion="Entrenamiento en pileta.",
        )
        self.club.disciplinas.add(self.disciplina)
        self.categoria = Categoria.objects.create(
            club=self.club,
            nombre="Sub 18",
            edad_minima=13,
            edad_maxima=17,
        )
        self.categoria.disciplina.add(self.disciplina)
        self.url = reverse(
            "clubes:gestion_crear_entrenador",
            args=[self.club.pk],
        )
        self.form_data = {
            "cuit_cuil": "20111222334",
            "email": "entrenador@example.com",
            "dni": "30123456",
            "nombre": "Carlos",
            "apellido": "Entrenador",
            "fecha_nacimiento": "1980-01-01",
            "telefono": "123456789",
            "direccion": "Calle 10",
            "experiencia": "8",
            "disciplinas": [self.disciplina.pk],
            "categorias": [self.categoria.pk],
        }

    def test_creates_account_profile_trainer_and_assignment(self):
        response = self.client.post(self.url, self.form_data)

        self.assertRedirects(
            response,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )
        usuario = Usuario.objects.get(cuit_cuil="20111222334")
        self.assertTrue(usuario.check_password("30123456"))
        self.assertEqual(usuario.perfil.nombre, "Carlos")
        self.assertEqual(usuario.perfil.dni, "30123456")

        entrenador = Entrenador.objects.get(usuario=usuario)
        self.assertEqual(entrenador.experiencia, 8)
        self.assertIn(self.club, entrenador.club.all())
        self.assertTrue(
            AsignacionEntrenador.objects.filter(
                entrenador=entrenador,
                perfil_club__club=self.club,
                disciplina=self.disciplina,
                categoria=self.categoria,
            ).exists()
        )
        self.assertTrue(
            PerfilClub.objects.filter(
                perfil=usuario.perfil,
                club=self.club,
                grupo_rol__name="ENTRENADOR",
            ).exists()
        )

    def test_creation_form_renders_the_four_steps_and_disciplines_category_link(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        for step in range(4):
            self.assertContains(response, f'data-wizard-step="{step}"')
        self.assertContains(response, 'type="password"')
        self.assertContains(
            response,
            f'data-disciplinas="{self.disciplina.pk}"',
        )

    def test_reuses_existing_account_and_trainer_without_overwriting_them(self):
        usuario = Usuario.objects.create_user(
            cuit_cuil="20999888777",
            email="existente@example.com",
            password="contraseña-anterior",
        )
        usuario.perfil.nombre = "Nombre original"
        usuario.perfil.apellido = "Apellido original"
        usuario.perfil.save()
        entrenador = Entrenador.objects.create(
            usuario=usuario,
            experiencia=12,
        )
        otro_club = Club.objects.create(
            nombre="Otro club",
            direccion="Avenida 20",
            telefono="987654321",
            email="otro@example.com",
            fecha_fundacion=date(2001, 1, 1),
        )
        entrenador.club.add(otro_club)

        datos = {
            **self.form_data,
            "cuit_cuil": usuario.cuit_cuil,
            "email": "",
            "dni": "",
            "nombre": "",
            "apellido": "",
            "fecha_nacimiento": "",
            "telefono": "",
            "direccion": "",
            "experiencia": "",
        }
        response = self.client.post(self.url, datos)

        self.assertRedirects(
            response,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )
        self.assertEqual(Usuario.objects.filter(cuit_cuil=usuario.cuit_cuil).count(), 1)
        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password("contraseña-anterior"))
        self.assertEqual(usuario.perfil.nombre, "Nombre original")
        self.assertEqual(entrenador.experiencia, 12)
        self.assertIn(self.club, entrenador.club.all())
        self.assertIn(otro_club, entrenador.club.all())
        self.assertEqual(
            AsignacionEntrenador.objects.filter(entrenador=entrenador).count(),
            1,
        )

    def test_reuses_existing_account_without_existing_trainer(self):
        usuario = Usuario.objects.create_user(
            cuit_cuil="20999888776",
            email="socio-existente@example.com",
            password="contraseña-anterior",
        )
        usuario.perfil.nombre = "Perfil existente"
        usuario.perfil.apellido = "Sin entrenador"
        usuario.perfil.save()
        datos = {
            **self.form_data,
            "cuit_cuil": usuario.cuit_cuil,
            "email": "",
            "dni": "",
            "nombre": "",
            "apellido": "",
            "fecha_nacimiento": "",
            "telefono": "",
            "direccion": "",
        }

        response = self.client.post(self.url, datos)

        self.assertRedirects(
            response,
            reverse("clubes:gestionar_club", args=[self.club.pk]),
        )
        usuario.refresh_from_db()
        entrenador = Entrenador.objects.get(usuario=usuario)
        self.assertEqual(Entrenador.objects.filter(usuario=usuario).count(), 1)
        self.assertEqual(usuario.perfil.nombre, "Perfil existente")
        self.assertTrue(usuario.check_password("contraseña-anterior"))
        self.assertEqual(entrenador.experiencia, 8)
        self.assertTrue(
            AsignacionEntrenador.objects.filter(
                entrenador=entrenador,
                perfil_club__perfil=usuario.perfil,
                perfil_club__club=self.club,
            ).exists()
        )

    def test_rejects_category_not_associated_with_selected_discipline(self):
        otra_disciplina = Disciplina.objects.create(
            nombre="Vóley",
            descripcion="Entrenamiento de vóley.",
        )
        self.club.disciplinas.add(otra_disciplina)
        otra_categoria = Categoria.objects.create(
            club=self.club,
            nombre="Primera",
            edad_minima=18,
            edad_maxima=40,
        )
        otra_categoria.disciplina.add(otra_disciplina)
        datos = {
            **self.form_data,
            "categorias": [otra_categoria.pk],
        }

        response = self.client.post(self.url, datos)

        self.assertEqual(response.status_code, 200)
        self.assertIn("categorias", response.context["form"].errors)
        self.assertFalse(Usuario.objects.filter(cuit_cuil="20111222334").exists())

    def test_assignment_model_rejects_category_from_another_club(self):
        usuario = Usuario.objects.create_user(
            cuit_cuil="20999888777",
            email="entrenador@example.com",
            password="test-password",
        )
        entrenador = Entrenador.objects.create(usuario=usuario, experiencia=1)
        entrenador.club.add(self.club)
        otro_club = Club.objects.create(
            nombre="Otro club",
            direccion="Avenida 20",
            telefono="987654321",
            email="otro@example.com",
            fecha_fundacion=date(2001, 1, 1),
        )
        categoria_ajena = Categoria.objects.create(
            club=otro_club,
            nombre="Sub 18",
            edad_minima=13,
            edad_maxima=17,
        )
        categoria_ajena.disciplina.add(self.disciplina)
        grupo_entrenador, _ = Group.objects.get_or_create(name="ENTRENADOR")
        membresia = PerfilClub.objects.create(
            perfil=usuario.perfil,
            club=self.club,
            grupo_rol=grupo_entrenador,
        )

        with self.assertRaises(ValidationError) as error:
            AsignacionEntrenador.objects.create(
                entrenador=entrenador,
                perfil_club=membresia,
                disciplina=self.disciplina,
                categoria=categoria_ajena,
            )

        self.assertIn("categoria", error.exception.message_dict)

    def test_club_management_lists_only_its_trainers_in_a_separate_tab(self):
        self.client.post(self.url, self.form_data)
        otro_club = Club.objects.create(
            nombre="Otro club",
            direccion="Avenida 20",
            telefono="987654321",
            email="otro@example.com",
            fecha_fundacion=date(2001, 1, 1),
        )
        otro_usuario = Usuario.objects.create_user(
            cuit_cuil="20999888776",
            email="otro-entrenador@example.com",
            password="test-password",
        )
        otro_usuario.perfil.nombre = "Entrenador de otro club"
        otro_usuario.perfil.save()
        otro_entrenador = Entrenador.objects.create(
            usuario=otro_usuario,
            experiencia=5,
        )
        otro_entrenador.club.add(otro_club)

        response = self.client.get(
            reverse("clubes:gestionar_club", args=[self.club.pk])
        )

        self.assertContains(response, "LISTADO DE SOCIOS")
        self.assertContains(response, "LISTADO DE ENTRENADORES")
        self.assertContains(response, "20111222334")
        self.assertNotContains(response, "20999888776")
