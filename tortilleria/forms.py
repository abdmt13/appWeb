from django import forms
from .models import Informacion_Tortilleria

class InformacionTortilleriaForm(forms.ModelForm):
    class Meta:
        model = Informacion_Tortilleria
        fields = ['nombre', 'direccion', 'horaInicio', 'horaFinal', 'imagen']  # Incluye el campo de imagen
