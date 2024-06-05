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
    nombre_estudio = models.CharField(max_length=255,null=True)
    genero = models.CharField(max_length=10,null=True)
    nombre_maquinaria = models.CharField(max_length=255,null=True)
    imagen_indexada = models.ImageField(upload_to='imagenes_indexadas/', null=True, blank=True)

    def __str__(self):
        return self.nombre_paciente

    def guardar_metadata(self):
        self.save()
        ds = pydicom.dcmread(self.archivo.path)
        self.nombre_paciente = ds.PatientName
        if hasattr(ds, 'StudyDate'):
            self.fecha = ds.StudyDate
        self.nombre_estudio = ds.InstitutionalDepartmentName if hasattr(ds, 'InstitutionalDepartmentName') else None
        self.genero = ds.PatientSex if hasattr(ds, 'PatientSex') else None
        self.nombre_maquinaria = ds.StationName if hasattr(ds, 'StationName') else None  # Asignar None si no se encuentra el nombre de la maquinaria
        self.save()

   
        if ds.pixel_array is not None:
            img = Image.fromarray(ds.pixel_array)
           
            if img.mode != "L":
                img = img.convert("L")
           
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            self.imagen_indexada.save('imagen_indexada.jpg', buffer)

