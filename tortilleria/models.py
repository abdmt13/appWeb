from django.db import models
from django.contrib.auth.models import User, Group



# Create your models here.
# modelo para guardar la informacion de la tortilleria
class Informacion_Tortilleria(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    horaInicio = models.TimeField()  # Hora de inicio
    horaFinal = models.TimeField()  # Hora de fin
    imagen = models.ImageField(upload_to='informacion/')  # Carpeta donde se almacenarán las imágenes

    def __str__(self):
        return f"{self.nombre} {self.direccion}"

    def __str__(self):
        return self.nombre
# ar
# modelo para guardar los empleados de la tortilleria
class HistorialEmpleado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    estatus = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.usuario.username} -> {self.grupo.name}"
    
    def eliminar(self):
        estatus=self.estatus=False
        self.save()
        return estatus
    
    def activar(self):
        estatus=self.estatus=True
        self.save()
        return estatus