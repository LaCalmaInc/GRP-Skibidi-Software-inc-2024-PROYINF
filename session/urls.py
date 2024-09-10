from django.urls import path
from .views import cargar_archivo_dicom, ver_archivos_dicom,buscar_maquinarias,index,detalles_maquinarias,archivos_por_dia,listar_dias,index,detalleImagen,visualizar_fotos_filtradas, home, signup, signout, signin


urlpatterns = [
    path('cargar/', cargar_archivo_dicom, name='cargar_archivo_dicom'),
    path('ver/', ver_archivos_dicom, name='ver_archivos_dicom'),
    path('visualizador/', buscar_maquinarias,name = 'buscar_maquinarias'),
    path('', home, name='home'),
    path('detalles/<str:nombre_paciente>/<str:nombre_maquinaria>/<str:nombre_estudio>/<str:protocol_name>', detalles_maquinarias, name='detalles_maquinarias'),
    path('archivos_por_dia/', listar_dias, name='listar_dias'),
    path('archivos_por_dia/<str:fecha>/', archivos_por_dia, name='archivos_por_dia'),
    path('detalle_imagen/' , detalleImagen, name='detalleImagen'),
    path('visualizar_fotos_filtradas/<str:nombre_paciente>/<str:nombre_maquinaria>/<str:nombre_estudio>/<str:protocol_name>/', visualizar_fotos_filtradas, name='visualizar_fotos_filtradas'),
    path('signup/', signup, name='signup'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    path('index/', index, name='index'),

]
