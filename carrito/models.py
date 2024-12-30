from django.db import models
from productos.models import Producto
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