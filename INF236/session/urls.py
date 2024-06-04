# En tu archivo urls.py

from django.urls import path
from .views import cargar_archivo_dicom, ver_archivos_dicom, index

urlpatterns = [
    path('cargar/', cargar_archivo_dicom, name='cargar_archivo_dicom'),
    path('ver/', ver_archivos_dicom, name='ver_archivos_dicom'),
    path('', index, name='index'),
]
