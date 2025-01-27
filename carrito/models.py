from django.db import models
from productos.models import Producto
from datosUser.models import Domicilio
from django.contrib.auth.models import User

# Create your models here.
class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrito")  # Cada usuario tiene un único carrito
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    

class ProductoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"Pedido {self.id} - {self.producto}"

    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    
    def resta(self):
        if self.cantidad > 1:  # Reduce la cantidad si es mayor que 1
            self.cantidad -= 1
            self.save()  # Guarda los cambios
        else:
            self.delete()  # Elimina el registro si la cantidad llega a 0
            
    def suma(self):
        self.cantidad +=1
        self.save()
        
    def eliminar(self):
        self.delete()
    
    def precio_total(self):
        return self.precio_unitario * self.cantidad
        
        
        
class Pedido(models.Model):
    TIPOPEDIDO = [
        ('D', 'Domicilio'),
        ('E', 'Express'),
        ('T', 'Tienda'),
    ]
    ESTATUS=[
        ('X','Cancelado'),
        ('E', 'Espera'),
        ('C', 'En curso'),
        ('F', 'Entregado'),
    ]
    
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)
    horario_entrega = models.DateTimeField(blank=True)
    tipo_pedido = models.CharField(max_length=1, choices=TIPOPEDIDO, default='D')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    estatus=models.CharField(max_length=1, choices=ESTATUS, default='P')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido {self.id} - {self.get_tipo_pedido_display()}"
    
    # def calcular_precio_total(user, id):
    #     productos = ProductoCarrito.objects.filter(user=user).filter(id=id)
    #     total = sum(item.producto.precio * item.cantidad for item in productos)
    #     return total

    
    
class Pedido_Producto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"
