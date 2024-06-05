# En tu archivo views.py

from django.shortcuts import render, redirect
from .models import ArchivoDicom
from .forms import ArchivoDicomForm, Busqueda_filtros
import pydicom

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



def ver_archivos_dicom(request):
    archivos_dicom = ArchivoDicom.objects.all()
    return render(request, 'ver_archivos_dicom.html', {'archivos_dicom': archivos_dicom})



def ver_imagenes_dicom(request):
    # Recuperar todos los archivos DICOM
    archivos_dicom = ArchivoDicom.objects.all()
    # Pasar la lista de archivos DICOM a la plantilla
    return render(request, 'ver_imagenes_dicom.html', {'archivos_dicom': archivos_dicom})

def filtros_dicom(request):
   
    if request.method == 'GET':

        forms= Busqueda_filtros(request.GET)
        archivos = ArchivoDicom.objects.all()
        
        if forms.is_valid():
            id_paciente= forms.cleaned_data.get('id_paciente')
            maquinaria= forms.cleaned_data.get('maquinaria')
            if id_paciente:
                archivos= archivos.filter(nombre_paciente__icontains=id_paciente)

            if maquinaria:
                archivos = archivos.filter(maquinaria__icontainer=maquinaria)

            return render(request,'buscar_archivo_dicom.html', {'archivos_dicom':archivos})

