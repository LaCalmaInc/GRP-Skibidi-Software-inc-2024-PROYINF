# En tu archivo urls.py

from django.urls import path
from .views import cargar_archivo_dicom, ver_archivos_dicom,buscar_maquinarias,index,ver_imagenes_dicom,detalles_maquinarias


urlpatterns = [
    path('cargar/', cargar_archivo_dicom, name='cargar_archivo_dicom'),
    path('ver/', ver_archivos_dicom, name='ver_archivos_dicom'),
    path('visualizador/', buscar_maquinarias,name = 'buscar_maquinarias'),
    path('', index, name='index'),
    path('detalles/<str:nombre_paciente>/<str:nombre_maquinaria>/', detalles_maquinarias, name='detalles_maquinarias'),

]
