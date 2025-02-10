from django.contrib import admin
from .models import Informacion_Tortilleria


@admin.register(Informacion_Tortilleria)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'horaInicio', 'horaFinal')  # Campos visibles en la lista


# Register your models here.
