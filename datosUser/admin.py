from django.contrib import admin
from .models import Domicilio

@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('nombreCompleto', 'calle', 'municipio', 'telefono')  # Campos visibles en la lista
    search_fields = ('nombreCompleto', 'municipio')  # Permite buscar por estos campos
    list_filter = ('municipio','nombreCompleto')  # Agrega filtros en la barra lateral


# Register your models here.
