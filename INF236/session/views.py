# En tu archivo views.py

from django.shortcuts import render, redirect,get_object_or_404
from .models import ArchivoDicom
from .forms import ArchivoDicomForm
from datetime import datetime
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
    archivos_dicom = ArchivoDicom.objects.all()
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
        'archivos_dicom': archivos_dicom, 
    }
    
    return render(request, 'ver_imagenes_dicom.html', context)

def detalles_maquinarias(request, nombre_paciente, nombre_maquinaria):
    archivos = ArchivoDicom.objects.filter(nombre_paciente=nombre_paciente, nombre_maquinaria=nombre_maquinaria)
    
    context = {
        'archivos': archivos,
        'nombre_paciente': nombre_paciente,
        'nombre_maquinaria': nombre_maquinaria,
    }
    
    return render(request, 'detalles_maquinarias_dicom.html', context)


def listar_dias(request):
    maquina_filtro = request.GET.get('maquina', None)
    archivos = ArchivoDicom.objects.all().order_by('-fecha_ingreso')
    
    if maquina_filtro:
        archivos = archivos.filter(nombre_maquinaria=maquina_filtro)
    
    dias = archivos.values('fecha_ingreso').distinct().order_by('-fecha_ingreso')
    
    context = {
        'dias': dias,
        'maquina_filtro': maquina_filtro
    }
    return render(request, 'listar_dias.html', context)

def archivos_por_dia(request, fecha):
    fecha_filtro = datetime.strptime(fecha, '%Y-%m-%d').date()
    archivos = ArchivoDicom.objects.filter(fecha_ingreso=fecha_filtro).order_by('-fecha_ingreso')
    context = {
        'archivos': archivos,
        'fecha_filtro': fecha_filtro
    }
    return render(request, 'inv.html', context)
def index(request):
    return render(request, 'index.html')