from django import forms
from django.forms import modelformset_factory
from django.forms import ModelForm
from .models import Producto
from django.contrib.auth.models import User

class productoForm(ModelForm):
    class Meta:      
        model=Producto
        fields=['tipo', 'nombre', 'descripcion', 'precio','existencia','estado']   
        
        
class BuscarProductoForm(forms.Form):
    codigo = forms.CharField(label="Código del producto", max_length=20) 
    
    
class AgregarInventarioForm(forms.Form):
    existencia= forms.DecimalField(label="Ingrese Cantidad", decimal_places=0, max_digits=3, help_text='4 o +4 o -2')  