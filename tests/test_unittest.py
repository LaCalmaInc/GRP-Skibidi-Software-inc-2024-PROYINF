import unittest
from unittest.mock import MagicMock, patch
import django
import os
from django.test import Client
from django.urls import reverse
from django.conf import settings



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INF236.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class TestAPIEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(username='testuser', password='password123')#caso1
        cls.client.login(username='testuser', password='password123')  # Inicia sesion para probar carga de archivos

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        User.objects.filter(username='test1').delete()
        User.objects.filter(username='test2').delete()

    #casos de prueba para login y registro
    def test_login_success(self):
        """Prueba de login con usuario existente"""
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)

    def test_register_password(self):
        """Prueba de pasword registro con contraseñas distintas"""
        response = self.client.post(reverse('signup'), {'username': 'test1', 'password1': 'password13','password2':'password123'})
        self.assertEqual(response.status_code, 200)
    
    def test_register_passwordOK(self):
        """Prueba de pasword registro todo OK"""
        response = self.client.post(reverse('signup'), {'username': 'test2', 'password1': 'password123', 'password2': 'password123'})
        self.assertEqual(response.status_code, 302)

    #casos de prueba para carga de archivos
    def test_subir_archivo_dicom_correcto(self):
        """Prueba para subir un archivo DICOM correcto"""
        
        with open('IMG-0002-00001.dcm', 'rb') as archivo:
            archivo_dicom = SimpleUploadedFile("archivo.dcm", archivo.read(), content_type="application/dicom")
            response = self.client.post(reverse('cargar_archivo_dicom'), {'archivos_dicom': archivo_dicom})
        self.assertEqual(response.status_code, 302)

    def test_subir_archivo_dicom_incorrecto(self):
        """Prueba para intentar subir un archivo que no es DICOM"""
        archivo_incorrecto = SimpleUploadedFile("archivo.txt", b"cualquier cosa que no sea DICOM", content_type="text/plain")
        response = self.client.post(reverse('cargar_archivo_dicom'), {'archivos_dicom': archivo_incorrecto})
        self.assertEqual(response.status_code, 200)
        

  
if __name__ == '__main__':
    unittest.main()