# En tu archivo views.py

from django.shortcuts import render, redirect
from .models import ArchivoDicom
from .forms import ArchivoDicomForm,Busqueda_filtros


def index(request):
    return render(request, 'index.html')


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
