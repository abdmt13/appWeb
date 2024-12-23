from django import forms
from django.forms import modelformset_factory
from django.forms import ModelForm
from .models import Producto
from django.contrib.auth.models import User

class productoForm(ModelForm):
    class Meta:      
        model=Producto
        fields=['tipo', 'nombre', 'descripcion', 'precio','existencia','estado']      