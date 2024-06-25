# En tu archivo urls.py

from django.urls import path
from .views import cargar_archivo_dicom, ver_archivos_dicom,buscar_maquinarias,index,detalles_maquinarias,archivos_por_dia,listar_dias,index,detalleImagen


urlpatterns = [
    path('cargar/', cargar_archivo_dicom, name='cargar_archivo_dicom'),
    path('ver/', ver_archivos_dicom, name='ver_archivos_dicom'),
    path('visualizador/', buscar_maquinarias,name = 'buscar_maquinarias'),
    path('', index, name='index'),
    path('detalles/<str:nombre_paciente>/<str:nombre_maquinaria>/<str:nombre_estudio>/<str:protocol_name>', detalles_maquinarias, name='detalles_maquinarias'),
    path('archivos_por_dia/', listar_dias, name='listar_dias'),
    path('archivos_por_dia/<str:fecha>/', archivos_por_dia, name='archivos_por_dia'),
    path('detalle_imagen/' , detalleImagen, name='detalleImagen')
]
