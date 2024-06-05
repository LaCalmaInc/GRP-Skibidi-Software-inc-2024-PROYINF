# forms.py

from django import forms
from .models import ArchivoDicom, Maquinaria


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ArchivoDicomForm(forms.Form):
    archivos_dicom = MultipleFileField()


class Busqueda_filtros(forms.Form):
    id_paciente= forms.CharField(required=False,max_length=12)
    maquinaria = forms.ModelChoiceField(queryset=Maquinaria.objects.all(), required =False)
   

