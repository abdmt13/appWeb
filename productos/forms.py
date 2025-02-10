from django import forms
from django.forms import modelformset_factory
from django.forms import ModelForm
from .models import Producto
from django.contrib.auth.models import User

class productoForm(ModelForm):
    class Meta:      
        model=Producto
        fields=['codigo', 'tipo', 'nombre', 'descripcion', 'precio','existencia','estado','imagen'] 

        widgets={'codigo': forms.TextInput(
            attrs={'class': 'form-control',
                'placeholder': 'ej: 01|producto01|nombre_del_producto'}),}
       
        
        
class BuscarProductoForm(forms.Form):
    codigo = forms.CharField(label="Código del producto", max_length=20) 
    
    
class AgregarInventarioForm(forms.Form):
    existencia= forms.DecimalField(label="Ingrese Cantidad", decimal_places=0, max_digits=3, help_text='4 o +4 o -2')  
    
class CantidadForm(forms.Form):
    cantidad=forms.DecimalField(label="Ingrese Cantidad", decimal_places=0, max_digits=2, help_text='de 1 a 99', initial=1)