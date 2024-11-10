from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Datos_personal(models.Model):
  
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    telefono = models.DecimalField(max_digits=10, decimal_places=0)
    municipio = models.CharField(max_length=200)
    estatus = models.BooleanField(default=True)
    fecha_nacimiento = models.DateField(auto_now=False)
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} {self.municipio}" 
    
# aqui puede poner 3 domuicilios   
class Domicilio(models.Model):
    nombreCompleto = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    entreCalle = models.CharField(max_length=50)
    referencia = models.TextField()
    telefono = models.CharField(max_length=15)
    municipio = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombreCompleto} {self.calle} {self.municipio}"
# esto es para poner como uno fijo siempre   y principal
class Domicilio_ruta(models.Model):
    info = models.ForeignKey(Domicilio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Nueva clave foránea para el usuario

    def __str__(self):
        return f"{self.info} - {self.user.username}"  # Muestra información del domicilio y el nombre de usuario