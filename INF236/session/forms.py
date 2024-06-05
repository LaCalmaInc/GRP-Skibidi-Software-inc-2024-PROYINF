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

class Busqueda_filtros(forms.Form):
    id_paciente = forms.CharField(required=False, max_length=12)
    maquinaria = forms.ModelChoiceField(queryset=ArchivoDicom.objects.all(), required=False, empty_label="Seleccione una maquinaria")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['maquinaria'].queryset = ArchivoDicom.objects.values_list('nombre_maquinaria', flat=True).distinct()