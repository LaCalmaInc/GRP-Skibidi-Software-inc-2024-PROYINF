# En tu archivo urls.py

from django.urls import path
from .views import cargar_archivo_dicom, ver_archivos_dicom, ver_imagenes_dicom, filtros_dicom


urlpatterns = [
    path('cargar/', cargar_archivo_dicom, name='cargar_archivo_dicom'),
    path('ver/', ver_archivos_dicom, name='ver_archivos_dicom'),
    path('visualizador/',ver_imagenes_dicom , name='ver_imagenes_dicom'),
    path('busqueda/', filtros_dicom,name = 'buscar_archivo_dicom'),
]
