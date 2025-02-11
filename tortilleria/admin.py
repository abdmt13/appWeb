from django.contrib import admin
from .models import Informacion_Tortilleria, HistorialEmpleado


@admin.register(Informacion_Tortilleria)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'horaInicio', 'horaFinal')  # Campos visibles en la lista

@admin.register(HistorialEmpleado)
class ProductoCarritoAdmin(admin.ModelAdmin):
	pass

# Register your models here.
