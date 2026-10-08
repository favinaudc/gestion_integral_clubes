from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Club, Socio

# Create your tests here.


class SocioCreateViewTests(TestCase):
	def setUp(self):
		self.club = Club.objects.create(
			nombre='Club de prueba',
			direccion='Calle 123',
			telefono='123456789',
			email='club@example.com',
			fecha_fundacion=date(2000, 1, 1),
		)

	def test_create_socio_without_usuario(self):
		create_url = reverse('clubes:crear_socio')
		response = self.client.get(create_url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content.count(b'<form'), 1)

		response = self.client.post(create_url, {
			'fecha_nacimiento': '1990-01-01',
			'club_id': self.club.pk,
		})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['Location'], reverse('clubes:listar_socios'))

		socio = Socio.objects.get()
		self.assertIsNone(socio.usuario)
		self.assertIsNotNone(socio.pk)
		self.assertEqual(str(socio), f'Socio #{socio.pk}')

	def test_socio_list_shows_details_and_combined_actions(self):
		socio = Socio.objects.create(
			fecha_nacimiento=date(1990, 1, 1),
			club_id=self.club,
			es_deportista=True,
			apto_medico=True,
		)
		response = self.client.get(reverse('clubes:listar_socios'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Acciones')
		self.assertContains(response, 'Sin usuario')
		self.assertContains(response, self.club.nombre)
		self.assertContains(response, 'Deportista')
		self.assertContains(response, 'Vigente')
		self.assertContains(response, reverse('clubes:editar_socio', args=[socio.pk]))
		self.assertContains(response, reverse('clubes:eliminar_socio', args=[socio.pk]))
		self.assertNotContains(response, '>Editar</th>')
		self.assertNotContains(response, '>Eliminar</th>')
