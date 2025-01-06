from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Producto(models.Model):
    TIPO = (
        ('u', 'Unidad'),
        ('p', 'Paquete'),
        ('m', 'Menudeo'),
    )
    tipo=models.CharField(max_length=1, choices=TIPO, blank=False, default='u', help_text='Tipo de producto')
    nombre=models.CharField(max_length=100, blank=False, help_text='Nombre del Producto', default='nombre')
    descripcion=models.TextField(max_length=100, blank=False, help_text='Nombre del Producto', default='descripcion')
    precio=models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    existencia=models.DecimalField(max_digits=9, decimal_places=0, blank=False)
    # imagen_referencia=models.ImageField()
    estado=models.BooleanField(help_text='disponibilidad')
    
    def __str__(self):
        return f"Pedido {self.nombre} - {self.precio}"

    def disminuir(self, cantidad=1):
        if self.existencia>1:
            self.existencia - cantidad
            self.save()
        else:
            pass
        
        
    def incrementar(self, cantidad):
        self.existencia + cantidad
        self.save()