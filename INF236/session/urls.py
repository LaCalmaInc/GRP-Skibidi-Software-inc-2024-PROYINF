# En tu archivo urls.py

from django.urls import path
from .views import cargar_archivo, ver_archivos

urlpatterns = [
    path('cargar/', cargar_archivo, name='cargar_archivo'),
    path('ver/', ver_archivos, name='ver_archivos'),
]
