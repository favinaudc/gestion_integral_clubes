from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Ciclo, CicloClub, Club, Socio


class SocioCreateViewTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nombre="Club de prueba",
            direccion="Calle 123",
            telefono="123456789",
            email="club@example.com",
            fecha_fundacion=date(2000, 1, 1),
        )

    def test_create_socio_without_usuario(self):
        create_url = reverse("clubes:crear_socio")# carga formulario
        response = self.client.get(create_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b"<form"), 1)

        response = self.client.post(
            create_url,
            {
                "fecha_nacimiento": "1990-01-01",
                "club_id": self.club.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("clubes:listar_socios"))

        socio = Socio.objects.get()
        self.assertIsNone(socio.usuario)
        self.assertIsNotNone(socio.pk)
        self.assertEqual(str(socio), f"Socio #{socio.pk}")

    # Que la vista que lista a los socios muestre correctamente la información detallada, las etiquetas de estado (si es deportista,
    # si tiene apto médico vigente, si no tiene usuario) y las acciones de Editar y Eliminar agrupadas
    # correctamente sin duplicar cabeceras innecesarias.

    def test_socio_list_shows_details_and_combined_actions(self):
        socio = Socio.objects.create(
            fecha_nacimiento=date(1990, 1, 1),
            club_id=self.club,
            es_deportista=True,
            apto_medico=True,
        )
        response = self.client.get(reverse("clubes:listar_socios"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acciones")
        self.assertContains(response, "Sin usuario")
        self.assertContains(response, self.club.nombre)
        self.assertContains(response, "Deportista")
        self.assertContains(response, "Vigente")
        self.assertContains(response, reverse("clubes:editar_socio", args=[socio.pk]))
        self.assertContains(response, reverse("clubes:eliminar_socio", args=[socio.pk]))
        self.assertNotContains(response, ">Editar</th>")
        self.assertNotContains(response, ">Eliminar</th>")


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
