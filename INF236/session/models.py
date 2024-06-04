# En tu archivo models.py

from django.db import models
from PIL import Image
import pydicom
import numpy as np
from io import BytesIO


class ArchivoDicom(models.Model):
    archivo = models.FileField(upload_to='archivos_dicom/')
    nombre_paciente = models.CharField(max_length=255)
    fecha = models.DateField(null=True, blank=True)  # Permitir que la fecha sea nula
    # Agrega más campos DICOM que desees guardar

    # Campo para la imagen indexada
    imagen_indexada = models.ImageField(upload_to='imagenes_indexadas/', null=True, blank=True)

    def __str__(self):
        return self.nombre_paciente

    def guardar_metadata(self):
        # Lee los metadatos DICOM
        ds = pydicom.dcmread(self.archivo.path)

        # Guarda la información en el modelo
        self.nombre_paciente = ds.PatientName
        if hasattr(ds, 'StudyDate'):
            self.fecha = ds.StudyDate
        # Agrega más campos según tus necesidades

        self.save()

        # Convierte la imagen DICOM a una imagen indexada y la guarda
        if ds.pixel_array is not None:
            img = Image.fromarray(ds.pixel_array)
            # Convierte a escala de grises si es necesario
            if img.mode != "L":
                img = img.convert("L")
            # Guarda la imagen indexada
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            self.imagen_indexada.save('imagen_indexada.jpg', buffer)

class Maquinaria(models.Model):
    nombre = models.CharField(max_length=100)   

    def __str__(self):
        return self.nombre
    
    