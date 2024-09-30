# En tu archivo models.py

from django.db import models
from PIL import Image,ImageEnhance, ImageOps
import pydicom
import numpy as np
from io import BytesIO



class ArchivoDicom(models.Model):
    archivo = models.FileField(upload_to='archivos_dicom/')
    nombre_paciente = models.CharField(max_length=255)
    fecha = models.DateField(null=True, blank=True)  # Permitir que la fecha sea nula
    nombre_estudio = models.CharField(max_length=255, null=True)
    genero = models.CharField(max_length=10, null=True)
    nombre_maquinaria = models.CharField(max_length=255, null=True)
    imagen_indexada = models.ImageField(upload_to='imagenes_indexadas/', null=True, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    
    # Nuevos campos
    patient_id = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    study_instance_uid = models.CharField(max_length=255, null=True, blank=True)
    study_time = models.TimeField(null=True, blank=True)
    study_id = models.CharField(max_length=255, null=True, blank=True)
    series_instance_uid = models.CharField(max_length=255, null=True, blank=True)
    series_number = models.IntegerField(null=True, blank=True)
    modality = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    manufacturer_model_name = models.CharField(max_length=255, null=True, blank=True)
    institution_name = models.CharField(max_length=255, null=True, blank=True)
    sop_instance_uid = models.CharField(max_length=255, null=True, blank=True)
    instance_number = models.IntegerField(null=True, blank=True)
    image_position_patient = models.CharField(max_length=255, null=True, blank=True)
    image_orientation_patient = models.CharField(max_length=255, null=True, blank=True)
    protocol_name = models.CharField(max_length=255, null=True, blank=True)
    body_part_examined = models.CharField(max_length=255, null=True, blank=True)
    performing_physician_name = models.CharField(max_length=255, null=True, blank=True)
    operators_name = models.CharField(max_length=255, null=True, blank=True)
    rows = models.IntegerField(null=True, blank=True)
    columns = models.IntegerField(null=True, blank=True)
    bits_allocated = models.IntegerField(null=True, blank=True)
    bits_stored = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre_paciente

    def guardar_metadata(self):
        self.save()
        ds = pydicom.dcmread(self.archivo.path)
        self.nombre_paciente = ds.PatientName if hasattr(ds, 'PatientName') else None
        self.patient_id = ds.PatientID if hasattr(ds, 'PatientID') else None
        self.fecha_nacimiento = ds.PatientBirthDate if hasattr(ds, 'PatientBirthDate') else None
        self.fecha = ds.StudyDate if hasattr(ds, 'StudyDate') else None
        self.study_instance_uid = ds.StudyInstanceUID if hasattr(ds, 'StudyInstanceUID') else None
        self.study_time = ds.StudyTime if hasattr(ds, 'StudyTime') else None
        self.study_id = ds.StudyID if hasattr(ds, 'StudyID') else None
        self.series_instance_uid = ds.SeriesInstanceUID if hasattr(ds, 'SeriesInstanceUID') else None
        self.series_number = ds.SeriesNumber if hasattr(ds, 'SeriesNumber') else None
        self.modality = ds.Modality if hasattr(ds, 'Modality') else None
        self.manufacturer = ds.Manufacturer if hasattr(ds, 'Manufacturer') else None
        self.manufacturer_model_name = ds.ManufacturerModelName if hasattr(ds, 'ManufacturerModelName') else None
        self.institution_name = ds.InstitutionName if hasattr(ds, 'InstitutionName') else None
        self.sop_instance_uid = ds.SOPInstanceUID if hasattr(ds, 'SOPInstanceUID') else None
        self.instance_number = ds.InstanceNumber if hasattr(ds, 'InstanceNumber') else None
        self.image_position_patient = ds.ImagePositionPatient if hasattr(ds, 'ImagePositionPatient') else None
        self.image_orientation_patient = ds.ImageOrientationPatient if hasattr(ds, 'ImageOrientationPatient') else None
        self.protocol_name = ds.ProtocolName if hasattr(ds, 'ProtocolName') else None
        self.body_part_examined = ds.BodyPartExamined if hasattr(ds, 'BodyPartExamined') else None
        self.performing_physician_name = ds.PerformingPhysicianName if hasattr(ds, 'PerformingPhysicianName') else None
        self.operators_name = ds.OperatorsName if hasattr(ds, 'OperatorsName') else None
        self.rows = ds.Rows if hasattr(ds, 'Rows') else None
        self.columns = ds.Columns if hasattr(ds, 'Columns') else None
        self.bits_allocated = ds.BitsAllocated if hasattr(ds, 'BitsAllocated') else None
        self.bits_stored = ds.BitsStored if hasattr(ds, 'BitsStored') else None
        self.nombre_estudio = ds.InstitutionalDepartmentName if hasattr(ds, 'InstitutionalDepartmentName') else None
        self.genero = ds.PatientSex if hasattr(ds, 'PatientSex') else None
        self.nombre_maquinaria = ds.StationName if hasattr(ds, 'StationName') else None
        self.save()

        if hasattr(ds, 'pixel_array'):
            img = Image.fromarray(ds.pixel_array)
            if img.mode != "L":
                img = img.convert("L")
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            self.imagen_indexada.save('imagen_indexada.jpg', buffer)


        def aplicar_negativo(self):
            ds = pydicom.dcmread(self.archivo.path)
            
            if hasattr(ds, 'pixel_array'):
                img = Image.fromarray(ds.pixel_array)
                
                if img.mode != "L":
                    img = img.convert("L")
            
                img = ImageOps.invert(img)
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0) 
                nombre_imagen = f'{self.pk}_imagen_negativa.jpg'
                self.imagen_indexada.save(nombre_imagen, buffer, save=False)
                self.save()
       
