from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Producto(models.Model):
    TIPO = (
        ('u', 'Unidad'),
        ('p', 'Paquete'),
        ('m', 'Menudeo'),
    )
    tipo=models.CharField(max_length=1, choices=TIPO, blank=False, null=False, default='u', help_text='Tipo de producto')
    nombre=models.CharField(max_length=100, blank=False, null=False, help_text='Nombre del Producto', default='nombre')
    descripcion=models.TextField(max_length=100, blank=False, null=False, help_text='Descripcion que ayude a los clientes a saber que estan comprando', default='descripcion')
    precio=models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    existencia=models.DecimalField(max_digits=9, decimal_places=0, blank=True, help_text='si el producto es menudeo, deje el campo vacio')
    # imagen_referencia=models.ImageField()
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Nuevo campo
    estado=models.BooleanField(help_text='disponibilidad')
    
    def __str__(self):
        return f"Pedido {self.nombre} - {self.precio}"

    def disminuir(self, cantidad=1):
        if self.existencia - cantidad>= 0:
            self.existencia -= cantidad  # Asigna el resultado de la resta
            self.save()
        else:
            pass

    def incrementar(self, cantidad):
        self.existencia += cantidad  # Asigna el resultado de la suma
        self.save()
    
    def save(self, *args, **kwargs):
        if self.tipo == 'm':
            self.existencia = 0
        super().save(*args, **kwargs)