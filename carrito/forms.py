from django.forms import ModelForm
from .models import Pedido, Pedido_Producto, Domicilio, Producto, ProductoCarrito

from django import forms
from django.contrib import messages
from .models import Pedido, Domicilio

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['domicilio', 'tipo_pedido']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibir el usuario en el formulario
        request = kwargs.pop('request', None)  # Recibir la solicitud
        super().__init__(*args, **kwargs)

        domicilios = Domicilio.objects.filter(user=user)
        if domicilios.exists():
            self.fields['domicilio'].queryset = domicilios
        else:
            self.fields.pop('domicilio')  # Ocultar el campo si no hay domicilios
            if request:
                messages.warning(request, "No tienes un domicilio registrado. Agrega uno para continuar.")

 
    
class PedidoProductoForm(ModelForm):
    class Meta:
        model = Pedido_Producto
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar todos los productos disponibles
        self.fields['producto'].queryset = Producto.objects.all()

class Checkbox(ModelForm):
    class Meta:
        model=ProductoCarrito
        fields=['seleccionado']