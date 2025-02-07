from django import forms
from django.forms import modelformset_factory
from django.forms import ModelForm
from .models import Domicilio
from django.contrib.auth.models import User



class datosPersonalesForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email']
        
class domicilioForm(ModelForm):
    def __init__(self, *args, **kwargs):
            # Extraer el usuario de los argumentos
            user = kwargs.pop('user', None)  # Extrae 'user' si está presente, de lo contrario, será None
            super().__init__(*args, **kwargs)  # Inicializa el formulario base

            if user:
                nombre = user.first_name
                apellido = user.last_name
                # Configurar el valor inicial de 'nombreCompleto'
                self.fields['nombreCompleto'].initial = f"{nombre} {apellido}"
    
    class Meta:
        
                
        model=Domicilio
        fields=['nombreCompleto', 'calle', 'entreCalle', 'referencia','telefono', 'municipio']
        
        widgets = {
            'nombreCompleto': forms.TextInput(attrs={
                'class': 'form-control',  # También puedes agregar clases CSS
            }),
            'calle': forms.NumberInput(attrs={
                'placeholder': 'Ejemplo: 16',
                'class': 'form-control',
            }),
            'entreCalle': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: 12 y 14',
                'class': 'form-control',
            }),
            'referencia': forms.Textarea(attrs={
                'placeholder': 'Ejemplo: Descripción de la ubicación: casa color morada, hay un arbolito afuera',
                'class': 'form-control',
                'rows': 3,  # Controla el tamaño del área de texto
            }),
            'telefono': forms.NumberInput(attrs={
                'placeholder': 'ejemplo: 9993954386',
                'class': 'form-control',
                  # Controla el tamaño del área de texto
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-control',
                'disabled': True,  # Deshabilita el campo
                # 'placeholder': 'Por el momento es el unicp municipio disponible',
            }),
        }
        
        
        
        

      