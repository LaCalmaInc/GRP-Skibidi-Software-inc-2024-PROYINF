# En tu archivo views.py

from django.shortcuts import render, redirect,get_object_or_404
from .models import ArchivoDicom
from django.conf import settings
from .forms import ArchivoDicomForm
from datetime import datetime
import pydicom
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse,HttpResponse
import os 
from .models import ArchivoDicom
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Image
from django.core.exceptions import ValidationError

@login_required
def cargar_archivo_dicom(request):
    if request.method == 'POST':
        form = ArchivoDicomForm(request.POST, request.FILES)
        if form.is_valid():
            archivos = request.FILES.getlist('archivos_dicom')
            for archivo in archivos:
                if not archivo.name.endswith('.dcm'):
                    form.add_error('archivos_dicom', 'El archivo debe ser en formato DICOM (.dcm).')
                    return render(request, 'cargar_archivo_dicom.html', {'form': form})
                archivo_dicom = ArchivoDicom(archivo=archivo)
                archivo_dicom.guardar_metadata()
            return redirect('cargar_archivo_dicom')  # Redirigir a la misma página después de cargar
    else:
        form = ArchivoDicomForm()
    return render(request, 'cargar_archivo_dicom.html', {'form': form})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if len(request.POST["password1"])>=8 and request.POST["password1"]== request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})
    
        else:
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match or length isn't enough (8 characters)."})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('index')

@login_required
def ver_imagen_negativa(request, nombre_paciente):
    archivos = ArchivoDicom.objects.filter(nombre_paciente=nombre_paciente, imagen_indexada__isnull=False)

    return render(request, 'tools_negative.html', {
        'nombre_paciente': nombre_paciente,
        'archivos': archivos,
    })

def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def ver_archivos_dicom(request):
    archivos_dicom = ArchivoDicom.objects.all()
    return render(request, 'ver_archivos_dicom.html', {'archivos_dicom': archivos_dicom})

@login_required
def ver_imagenes_dicom(request):
    archivos_dicom = ArchivoDicom.objects.all()
    return render(request, 'ver_imagenes_dicom.html', {'archivos_dicom': archivos_dicom})

def buscar_maquinarias(request):
    nombre = request.GET.get('nombre', '')
    maquinaria = request.GET.get('maquinaria', '')
    estudio = request.GET.get('estudio','')
    protocolo = request.GET.get('protocolo','')
    archivos = ArchivoDicom.objects.all()
    archivos_dicom = ArchivoDicom.objects.all()
    if nombre:
        archivos = archivos.filter(nombre_paciente__icontains=nombre)
    if maquinaria:
        archivos = archivos.filter(nombre_maquinaria__icontains=maquinaria)
    if estudio:
        archivos = archivos.filter(nombre_estudio__icontains=estudio)
    if protocolo:
        archivos = archivos.filter(protocol_name__icontains=protocolo)

    
     
    archivos_serializados = serialize('json', archivos)
    archivos_json = json.loads(archivos_serializados)    
    maquinarias = ArchivoDicom.objects.values_list("nombre_maquinaria", flat=True).distinct()
    estudios = ArchivoDicom.objects.values_list("nombre_estudio", flat=True).distinct()
    protocolos = ArchivoDicom.objects.values_list("protocol_name", flat=True).distinct()
    archivos = archivos.values('nombre_paciente', 'nombre_maquinaria','nombre_estudio','protocol_name').distinct()
    

    context = {
        'archivos': archivos,
        'maquinarias': maquinarias,
        'estudios':estudios,
        'protocolos': protocolos,
        'nombre': nombre,
        'protocolo_id':protocolo,
        'maquinaria_id': maquinaria, 
        'estudio_id': estudio,
        'archivos_dicom': archivos_dicom, 
    }
    
    return render(request, 'ver_imagenes_dicom.html', context)


def tools(request):
    nombre = request.GET.get('nombre', '')
    maquinaria = request.GET.get('maquinaria', '')

    archivos = ArchivoDicom.objects.all()
    archivos_dicom = ArchivoDicom.objects.all()
    if nombre:
        archivos = archivos.filter(nombre_paciente__icontains=nombre)
    if maquinaria:
        archivos = archivos.filter(nombre_maquinaria__icontains=maquinaria)


    
  
    maquinarias = ArchivoDicom.objects.values_list("nombre_maquinaria", flat=True).distinct()
    archivos = archivos.values('nombre_paciente', 'nombre_maquinaria','nombre_estudio','protocol_name').distinct()
    

    context = {
        'archivos': archivos,
        'maquinarias': maquinarias,
        'nombre': nombre,
        'maquinaria_id': maquinaria, 
        'archivos_dicom': archivos_dicom, 
    }
    
    return render(request, 'tools.html', context)

def detalles_maquinarias(request, nombre_paciente, nombre_maquinaria,protocol_name,nombre_estudio):
    archivos = ArchivoDicom.objects.filter(nombre_paciente=nombre_paciente, nombre_maquinaria=nombre_maquinaria, nombre_estudio = nombre_estudio, protocol_name = protocol_name)
    
    context = {
        'archivos': archivos,
        'nombre_paciente': nombre_paciente,
        'nombre_maquinaria': nombre_maquinaria,
        'protocol_name':protocol_name,
        'nombre_estudio':nombre_estudio
    }
    
    return render(request, 'detalles_maquinarias_dicom.html', context)



def visualizar_fotos_filtradas(request, nombre_paciente, nombre_maquinaria, nombre_estudio, protocol_name):
    archivos = ArchivoDicom.objects.filter(
        nombre_paciente=nombre_paciente, 
        nombre_maquinaria=nombre_maquinaria, 
        nombre_estudio=nombre_estudio, 
        protocol_name=protocol_name
    )

    context = {
        'archivos': archivos,
        'nombre_paciente': nombre_paciente,
        'nombre_maquinaria': nombre_maquinaria,
        'protocol_name': protocol_name,
        'nombre_estudio': nombre_estudio
    }
    
    return render(request, 'visualizar_fotos_filtradas.html', context)

def visualizar_fotos_filtradas_neg(request, nombre_paciente, nombre_maquinaria):

    archivos = ArchivoDicom.objects.filter(
            nombre_paciente=nombre_paciente, 
            nombre_maquinaria=nombre_maquinaria
            
    )

    context = {

        'archivos': archivos,
        'nombre_paciente': nombre_paciente,
        'nombre_maquinaria': nombre_maquinaria
        }
    return render(request,'tools.html',context)


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

def detalleImagen(request):
    return render(request,'detalle_imagen.html')

