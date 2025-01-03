from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Carrito, ProductoCarrito
# from django.contrib.auth.models import User
from productos.models import Producto

# Create your views here.

def homeCarrito(request):
    try:
        # Obtén el carrito del usuario
        carritoUser = Carrito.objects.get(user=request.user)
        # Filtra los productos del carrito
        productos = ProductoCarrito.objects.filter(carrito=carritoUser)
    except Carrito.DoesNotExist:
        # Si no existe un carrito, los productos serán una lista vacía
        carritoUser=None
        productos = []

    # Renderiza la plantilla con el contexto
    print(f"esto es lo que trae carritoUser{carritoUser} y esto trae productos{productos}")
    return render(request, 'carrito/homeCarrito.html', context={'productos': productos})


def agregarCarrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    detalle, created = ProductoCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'precio_unitario': producto.precio}
    )
    if not created:
        detalle.cantidad += 1
    detalle.subtotal = detalle.cantidad * detalle.precio_unitario
    detalle.save()

    messages.success(request, f'{producto.nombre} se ha agregado al carrito.')
    return redirect('homeCarrito')
        
        
def restaCarrito(request, producto_id):
    producto=ProductoCarrito.objects.get(id=producto_id)
    producto.resta()
    return redirect('homeCarrito')

def sumaCarrito(request, producto_id):
    producto=ProductoCarrito.objects.get(id=producto_id)
    producto.suma()
    print(f'esta cantidad tiene el producto en el carrito {producto.cantidad}')
    return redirect("homeCarrito")

def eliminar_del_carrito(request, producto_id):
    producto=ProductoCarrito.objects.get(id=producto_id)
    producto.eliminar()
    return redirect ('homeCarrito')


# def comprar(request, producto_id):
    