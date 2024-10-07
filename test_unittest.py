import unittest
import django
import os
from django.test import Client
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INF236.settings')
django.setup()

from django.contrib.auth.models import User

class TestAPIEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()  # Cliente de pruebas de Django
        cls.user = User.objects.create_user(username='testuser', password='password123')#caso1


    @classmethod
    def tearDownClass(cls):
        """Este método se ejecuta una vez después de todos los tests"""
        super().tearDownClass()
        # Limpia los datos creados para las pruebas, si es necesario
        cls.user.delete()
        User.objects.filter(username='GENERAL XABIER GOMEZ').delete()
        User.objects.filter(username='gragas').delete()

    #casos de prueba para login y registro
    def test_login_success(self):
        """Prueba de login"""
        response = self.client.post('/signin/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)

    def test_register_password(self):
        """Prueba de pasword registro"""
        response = self.client.post('/signup/', {'username': 'GENERAL XABIER GOMEZ', 'password1': 'password13','password2':'password123'})
        self.assertEqual(response.status_code, 200)
    
    def test_register_passwordOK(self):
        """Prueba de pasword registro"""
        response = self.client.post('/signup/', {'username': 'gragas', 'password1': 'password123','password2':'password123'})
        self.assertEqual(response.status_code, 302)

    #casos de prueba para suputamadre

  
if __name__ == '__main__':
    unittest.main()
