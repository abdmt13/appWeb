from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal 
from django.contrib import messages
from .models import Carrito, ProductoCarrito
# from django.contrib.auth.models import User
from .forms import PedidoForm, PedidoProductoForm
from productos.forms import CantidadForm
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


def gestionarAccion(request, producto_id):
    if request.method =='POST':
        # def cantidad():
        cantidad=CantidadForm(request.POST)
        
        if cantidad.is_valid():
            cantidad_value = cantidad.cleaned_data['cantidad']
            request.session['cantidad_value'] = float(cantidad_value)  # Guardamos el valor en la sesión
            request.session.save()
        cantidad_value = request.session.get('cantidad_value', None) 
        
       
        cantidad_value = Decimal(cantidad_value)  # Convertirlo de nuevo a Decimal
        

        
       
        form = PedidoForm(user=request.user)
        # cantidad.cleaned_data['cantidad']
        # print(f'esto trae la cantidad {cantidad}')
            
                
        productoReal = get_object_or_404(Producto, id=producto_id)
        accion = request.POST.get("accion")
        if accion == 'agregar':
            
            carrito, created = Carrito.objects.get_or_create(user=request.user)
            detalle, created = ProductoCarrito.objects.get_or_create(
                carrito=carrito,
                producto=productoReal,
                defaults={'precio_unitario': productoReal.precio},
            )
            
            if created:
                # Si el producto no existía, asignar la cantidad del formulario
                detalle.cantidad = cantidad_value
            else:
                # Si ya existía, sumar la cantidad del formulario
                detalle.cantidad += cantidad_value
            
            # if not created:
            #     # Si el formulario no es válido y el producto ya existía, sumar 1
            #     detalle.cantidad += 1
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario
            detalle.save()

            messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
            return redirect('homeCarrito')
        
        # aqui se compra desde producto home
        elif accion=='comprar':
            
            datos_productos={'producto':productoReal,
                            'unidad':cantidad_value}
            return render(request, 'carrito/compraCarrito.html', {
                'form': form,
                'producto': datos_productos
            })
            
            
        else:
            print('estoy enviando los datos del form y saltando todos los demas botones')
            try:
                form = PedidoForm(request.POST, user=request.user)
                print(f'esto tra el form: {form}')
                
                precio_total= cantidad_value * productoReal.precio
                print(f'esto tra el precio total: {precio_total}')
                if form.is_valid():
                
                #aqui comienza el bloque donde creamos una instancia de nuestro modelo pedido
              # Crear un objeto Pedido sin guardarlo aún
                    pedido = form.save(commit=False)
                
            # #     # Asignar valores adicionales al pedido
                    pedido.user = request.user
                    pedido.precio_total = precio_total
                    pedido.estatus = 'E'  # Estado "Espera"
                    pedido.horario_entrega = now()
                
            # #     # Guardar definitivamente en la base de datos
                    pedido.save()
                
            # #     #aqui comienza el bloque donde creamos una instancia de nuestro modelo pedido_producto
                    form=PedidoProductoForm()
                    pedidoProducto=form.save(commit=False)
                    pedidoProducto.pedido=pedido
                    pedidoProducto.producto=productoReal
                
                    pedidoProducto.cantidad=cantidad_value
            # #     #este atributo es de nuestro modelo Producto
            # #     productoCarrito.producto.disminuir(productoCarrito.cantidad)
            # #     #guardamos en la bd el producto o productos
                    pedidoProducto.save()
                    print('se guardo la compra y el producto')
                    return redirect('home')
            # 
                
            except:
                print('algo salio mal')
                return redirect('homeProductos')
                
            
            
        
        
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
                #aqui comienza el bloque donde creamos una instancia de nuestro modelo pedido
                # Crear un objeto Pedido sin guardarlo aún
                pedido = form.save(commit=False)
                
                # Asignar valores adicionales al pedido
                pedido.user = request.user
                pedido.precio_total = precio_total
                pedido.estatus = 'E'  # Estado "Espera"
                pedido.horario_entrega = now()
                
                # Guardar definitivamente en la base de datos
                pedido.save()
                
                #aqui comienza el bloque donde creamos una instancia de nuestro modelo pedido_producto
                form=PedidoProductoForm()
                pedidoProducto=form.save(commit=False)
                pedidoProducto.pedido=pedido
                pedidoProducto.producto=productoReal
                
                pedidoProducto.cantidad=productoCarrito.cantidad
                #este atributo es de nuestro modelo Producto
                productoCarrito.producto.disminuir(productoCarrito.cantidad)
                #guardamos en la bd el producto o productos
                pedidoProducto.save()
                #eliminamos del carrito
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
