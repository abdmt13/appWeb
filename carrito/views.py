from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Carrito, ProductoCarrito
# from django.contrib.auth.models import User
from .forms import PedidoForm, PedidoProductoForm
from productos.models import Producto
from django.utils.timezone import now

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


def comprar(request, producto_id, origen=None):
    if origen == 'fromhomecarrito':
        try:
            # este trae el producto que se quiere comprar
            productoCarrito = ProductoCarrito.objects.get(id=producto_id)
            productoReal=productoCarrito.producto
            # trae el carrito del usuario
            carritoUser = Carrito.objects.get(user=request.user)
            # trae los productos del carrito 
            carrito=ProductoCarrito.objects.filter(carrito=carritoUser)
        except ProductoCarrito.DoesNotExist:
            return render(request, 'carrito/homeCarrito.html', {'mensaje': 'Producto no encontrado.'})

        if request.method == "POST":
            precio_total = productoCarrito.precio_total()  # Calcular el precio total
            form = PedidoForm(request.POST, user=request.user)  # Formulario con datos del usuario
            
            if form.is_valid():
                # Crear un objeto Pedido sin guardarlo aún
                pedido = form.save(commit=False)
                
                # Asignar valores adicionales al pedido
                pedido.user = request.user
                pedido.precio_total = precio_total
                pedido.estatus = 'E'  # Estado "Espera"
                pedido.horario_entrega = now()
                
                # Guardar definitivamente en la base de datos
                pedido.save()
                
                
                form=PedidoProductoForm()
                pedidoProducto=form.save(commit=False)
                pedidoProducto.pedido=pedido
                pedidoProducto.producto=productoReal
                
                pedidoProducto.cantidad=productoCarrito.cantidad
                pedidoProducto.save()
                productoCarrito.eliminar()
                
                
                return render(request, 'carrito/homeCarrito.html', context={'mensaje': 'Su pedido está en espera.', 'productos':carrito})
            else:
                # Si el formulario no es válido
                return render(request, 'carrito/compraCarrito.html', {
                    'form': form,
                    'producto': carrito,
                    'error': 'Formulario inválido. Por favor, verifique los datos.'
                })
        
        else:  # Si es una solicitud GET
            datos_producto = {
                'producto': productoCarrito.producto,
                'unidad': productoCarrito.cantidad
            }
            form = PedidoForm(user=request.user)  # Inicializar formulario vacío
            
            return render(request, 'carrito/compraCarrito.html', {
                'form': form,
                'producto': datos_producto
            })
