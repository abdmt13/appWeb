from django.contrib import admin
from .models import Carrito, ProductoCarrito, Pedido, Pedido_Producto


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
	pass

@admin.register(ProductoCarrito)
class ProductoCarritoAdmin(admin.ModelAdmin):
	pass


class PedidoProductoInline(admin.TabularInline):
    model = Pedido_Producto
    extra = 1  # Número de filas adicionales en blanco

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('user', 'domicilio', 'tipo_pedido', 'estatus', 'productos_y_cantidades')
    search_fields = ('user__username', 'domicilio')
    list_filter = ('user', 'domicilio')
    inlines = [PedidoProductoInline]  # Agregar los productos dentro del pedido

    def productos_y_cantidades(self, obj):
        productos = Pedido_Producto.objects.filter(pedido=obj).select_related('producto')
        return ", ".join([f"{p.producto.nombre} ({p.cantidad})" for p in productos])

    productos_y_cantidades.short_description = "Productos y Cantidades"

# @admin.register(Pedido)
# class Pedido(admin.ModelAdmin):
#     list_display = ('user', 'domicilio', 'tipo_pedido', 'estatus')  # Campos visibles en la lista
#     search_fields = ('user', 'domicilio')  # Permite buscar por estos campos
#     list_filter = ('user','domicilio')  # Agrega filtros en la barra lateral

# @admin.register(Pedido_Producto)
# class Pedido_producto(admin.ModelAdmin):
#     list_display = ('pedido', 'producto', 'cantidad')  # Campos visibles en la lista
#     search_fields = ('pedido', )  # Permite buscar por estos campos
#     list_filter = ('pedido',)  # Agrega filtros en la barra lateral
# Register your models here.
