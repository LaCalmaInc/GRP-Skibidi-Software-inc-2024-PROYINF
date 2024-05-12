# En tu archivo forms.py

from django import forms
from .models import ArchivoDicom



class ArchivoDicomForm(forms.ModelForm):
    class Meta:
        model = ArchivoDicom
        fields = ['archivo']  # Solo mostramos el campo archivo en el formulario
        widgets = {
            'archivo': forms.FileInput(attrs={'accept': '.dcm'})
        }