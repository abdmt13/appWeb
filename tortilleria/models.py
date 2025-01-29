from django.db import models

# Create your models here.
class Informacion_Tortilleria(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    horaInicio = models.TimeField()  # Hora de inicio
    horaFinal = models.TimeField()  # Hora de fin
    imagen = models.ImageField(upload_to='productos/')  # Carpeta donde se almacenarán las imágenes

    def __str__(self):
        return self.nombre