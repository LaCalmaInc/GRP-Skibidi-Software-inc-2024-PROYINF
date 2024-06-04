# En tu archivo forms.py

from django import forms
from .models import ArchivoDicom, Maquinaria



class ArchivoDicomForm(forms.ModelForm):
    class Meta:
        model = ArchivoDicom
        fields = ['archivo']  # Solo mostramos el campo archivo en el formulario
        widgets = {
            'archivo': forms.FileInput(attrs={'accept': '.dcm'})
        }

class Busqueda_filtros(forms.Form):
    id_paciente= forms.CharField(required=False,max_length=12)
    maquinaria = forms.ModelChoiceField(queryset=Maquinaria.objects.all(), required =False)
   