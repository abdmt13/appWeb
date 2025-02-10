from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('codigo','tipo', 'nombre', 'precio', 'existencia')  # Campos visibles en la lista
    search_fields = ('codigo', 'nombre')  # Permite buscar por estos campos
    list_filter = ('codigo','nombre')  # Agrega filtros en la barra lateral


# Register your models here.
