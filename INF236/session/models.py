# En tu archivo models.py

from django.db import models

class Archivo(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='archivos/')

    def __str__(self):
        return self.nombre
    
    def url(self):
        return self.archivo.url
