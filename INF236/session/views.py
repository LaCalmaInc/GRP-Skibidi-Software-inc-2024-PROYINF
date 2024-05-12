# En tu archivo views.py

from django.shortcuts import render, redirect
from .forms import ArchivoForm
from .models import Archivo

def cargar_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cargar_archivo')
    else:
        form = ArchivoForm()
    return render(request, 'cargar_archivo.html', {'form': form})

def ver_archivos(request):
    archivos = Archivo.objects.all()
    return render(request, 'ver_archivos.html', {'archivos': archivos})
