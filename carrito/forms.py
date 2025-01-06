from django.forms import ModelForm
from .models import Pedido, Pedido_Producto, Domicilio, Producto

class PedidoForm(ModelForm):
    class Meta:      
        model = Pedido
        fields = ['domicilio', 'tipo_pedido']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibir el usuario en el formulario
        super().__init__(*args, **kwargs)
        if user:
            self.fields['domicilio'].queryset = Domicilio.objects.filter(user=user)
 
    
class PedidoProductoForm(ModelForm):
    class Meta:
        model = Pedido_Producto
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar todos los productos disponibles
        self.fields['producto'].queryset = Producto.objects.all()
