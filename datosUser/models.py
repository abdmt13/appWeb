from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
# aqui puede poner 3 domuicilios   
class Domicilio(models.Model):
    MUNICIPIO=[
        ('E','Ekmul'),
        ('T','Tixkokob'),
        ('N','Nolo'),
    ]
    nombreCompleto = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    entreCalle = models.CharField(max_length=50)
    referencia = models.TextField()
    telefono = models.CharField(max_length=15)
    municipio = models.CharField(max_length=1, choices=MUNICIPIO, default='E')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombreCompleto} {self.calle} {self.municipio}"
# esto es para poner como uno fijo siempre   y principal
