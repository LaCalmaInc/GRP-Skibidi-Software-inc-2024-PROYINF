# En tu archivo views.py

from django.shortcuts import render, redirect,get_object_or_404
from .models import ArchivoDicom
from .forms import ArchivoDicomForm, Busqueda_filtros
import pydicom
from django.urls import reverse

def cargar_archivo_dicom(request):
    if request.method == 'POST':
        form = ArchivoDicomForm(request.POST, request.FILES)
        if form.is_valid():
            archivos = request.FILES.getlist('archivos_dicom')
            for archivo in archivos:
                archivo_dicom = ArchivoDicom(archivo=archivo)
                archivo_dicom.guardar_metadata()
            return redirect('cargar_archivo_dicom')  # Redirigir a la misma página después de cargar
    else:
        form = ArchivoDicomForm()
    return render(request, 'cargar_archivo_dicom.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def ver_archivos_dicom(request):
    archivos_dicom = ArchivoDicom.objects.all()
    return render(request, 'ver_archivos_dicom.html', {'archivos_dicom': archivos_dicom})

def ver_imagenes_dicom(request):
    archivos_dicom = ArchivoDicom.objects.all()
    return render(request, 'ver_imagenes_dicom.html', {'archivos_dicom': archivos_dicom})

def buscar_maquinarias(request):
    nombre = request.GET.get('nombre', '')
    maquinaria = request.GET.get('maquinaria', '')
    archivos = ArchivoDicom.objects.all()
    
    if nombre:
        archivos = archivos.filter(nombre_paciente__icontains=nombre)
    if maquinaria:
        archivos = archivos.filter(nombre_maquinaria__icontains=maquinaria)
    
    maquinarias = ArchivoDicom.objects.values_list("nombre_maquinaria", flat=True).distinct()
    archivos = archivos.values('nombre_paciente', 'nombre_maquinaria').distinct()

    context = {
        'archivos': archivos,
        'maquinarias': maquinarias,
        'nombre': nombre,
        'maquinaria_id': maquinaria,  
    }
    
    return render(request, 'buscar_archivos_dicom.html', context)

def detalles_maquinarias(request, nombre_paciente, nombre_maquinaria):
    archivos = ArchivoDicom.objects.filter(nombre_paciente=nombre_paciente, nombre_maquinaria=nombre_maquinaria)
    
    context = {
        'archivos': archivos,
        'nombre_paciente': nombre_paciente,
        'nombre_maquinaria': nombre_maquinaria,
    }
    
    return render(request, 'detalles_maquinarias_dicom.html', context)
