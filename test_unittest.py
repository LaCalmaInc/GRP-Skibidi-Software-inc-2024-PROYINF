import unittest
import django
import os
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INF236.settings')

django.setup()

class TestAPIEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()  # Cliente de pruebas de Django

    def test_some_endpoint(self):
        response = self.client.get('/index/')  # Cambia '/some-url/' por una URL real de tu app
        self.assertEqual(response.status_code, 200)
        self.assertIn('</footer>\n', response.content.decode().strip())
  
if __name__ == '__main__':
    unittest.main()
