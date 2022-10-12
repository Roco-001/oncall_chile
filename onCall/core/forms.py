from django import forms
from .models import GuardiaEspecialista, Guardia
from django.utils import  timezone
now = timezone.now








class GuardiaEspecialistaForm(forms.ModelForm):
    class Meta:
        model = GuardiaEspecialista
        fields = ['name', 'fecha_inicio','fecha_fin','guardia']
        widgets = {
            'name': forms.Select(
                attrs={'class': 'form-control mt-3',  'required': 'True', 'type':'text'}),
            'fecha_inicio': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class': 'form-control mt-3'}),
            'fecha_fin': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                attrs={'class': 'form-control mt-3'}),
            'guardia': forms.SelectMultiple(attrs={'class': 'form-control-file mt-3'}),
        }

        labels = {
            'fecha_inicio': 'Fecha de Inicio',
        }

