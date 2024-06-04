# En tu archivo views.py

from django.shortcuts import render, redirect
from .models import ArchivoDicom
from .forms import ArchivoDicomForm

def cargar_archivo_dicom(request):
    if request.method == 'POST':
        form = ArchivoDicomForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_dicom = form.save(commit=False)
            archivo_dicom.guardar_metadata()  # Guarda los metadatos
            archivo_dicom.save()
            return redirect('ver_archivos_dicom')
    else:
        form = ArchivoDicomForm()
    return render(request, 'cargar_archivo_dicom.html', {'form': form})


def cargar_archivo_dicom(request):
    if request.method == 'POST':
        form = ArchivoDicomForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_dicom = form.save()
            archivo_dicom.guardar_metadata()  # Guarda los metadatos
            return redirect('cargar_archivo_dicom')  # Redirige a la misma vista
    else:
        form = ArchivoDicomForm()
    return render(request, 'cargar_archivo_dicom.html', {'form': form})

def ver_archivos_dicom(request):
    archivos_dicom = ArchivoDicom.objects.all()
    return render(request, 'ver_archivos_dicom.html', {'archivos_dicom': archivos_dicom})


def ver_imagenes_dicom(request):
    # Recuperar todos los archivos DICOM
    archivos_dicom = ArchivoDicom.objects.all()
    # Pasar la lista de archivos DICOM a la plantilla
    return render(request, 'ver_imagenes_dicom.html', {'archivos_dicom': archivos_dicom})