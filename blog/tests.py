from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Publicacion

# Create your tests here.
class PruebasBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username='usuarioprueba',
            email='prueba@email.com',
            password='secreto'
        )
        cls.pub = Publicacion.objects.create(
            titulo = 'Un buen título',
            cuerpo = 'Muy buen contenido',
            autor = cls.usuario,
        )

    def test_modelo_publicacion(self):
        self.assertEqual(self.pub.titulo, 'Un buen título')
        self.assertEqual(self.pub.cuerpo, 'Muy buen contenido')
        self.assertEqual(self.pub.autor.username, 'usuarioprueba')
        self.assertEqual(str(self.pub), 'Un buen título')
        self.assertEqual(self.pub.get_absolute_url(), '/pub/1/')

    def test_url_existe_en_ubicacion_correcta_listview(self):
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)

    def test_url_existe_en_ubicacion_correcta_detailview(self):
        respuesta = self.client.get('/pub/1/')
        self.assertEqual(respuesta.status_code, 200)

    def test_publicacion_listview(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Muy buen contenido')
        self.assertTemplateUsed(respuesta, 'inicio.html')
    
    def test_publicacion_detailview(self):
        respuesta = self.client.get(reverse('detalle_pub', kwargs={'pk': self.pub.pk}))
        sin_respuesta = self.client.get('/pub/100000/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(sin_respuesta.status_code, 404)
        self.assertContains(respuesta, 'Un buen título')
        self.assertTemplateUsed(respuesta, 'detalle_pub.html')

    def test_vista_crear_publicacion(self):
        respuesta = self.client.post(
            reverse('nueva_pub'), {
                "titulo": "Nuevo titulo",
                "cuerpo": "Nuevo texto",
                "autor":self.usuario.id
            })
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Publicacion.objects.last().titulo, "Nuevo titulo")
        self.assertEqual(Publicacion.objects.last().cuerpo, "Nuevo texto")

    def test_vista_editar(self):
        respuesta = self.client.post(
            reverse('editar_pub', args=[1]),
            {
                'titulo': 'titulo modificado',
                'cuerpo': 'texto modificado',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Publicacion.objects.last().titulo, 'titulo modificado')
        self.assertEqual(Publicacion.objects.last().cuerpo, 'texto modificado')

    def test_vista_eliminar(self):
        respuesta = self.client.post(reverse('eliminar_pub', args=[1]))
        self.assertEqual(respuesta.status_code, 302)
