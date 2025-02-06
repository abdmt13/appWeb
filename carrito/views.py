from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal 
from django.contrib import messages
from .models import Carrito, ProductoCarrito, Producto, Pedido, Pedido_Producto
from django.views.generic import ListView
# from django.contrib.auth.models import User
from .forms import PedidoForm, PedidoProductoForm, Checkbox
from productos.forms import CantidadForm
from django.utils.timezone import now

# Create your views here.
@login_required
def homeCarrito(request):
    if request.method=='GET':
        try:
            seleccionform=Checkbox()
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
        return render(request, 'carrito/homeCarrito.html', context={'productos': productos, 'seleccionform':seleccionform,
                                                                    'mensaje':'hola usuario'
                                                                    })


class ProductosListaViews(LoginRequiredMixin,ListView):
    model=Producto
    template_name = 'carrito/menuProducto.html'  # Tu plantilla
    context_object_name = 'productos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formCantidad']=CantidadForm()
        # context['form'] = BuscarProductoForm()  # Agrega el formulario al contexto
        
        return context


            
            
        
@login_required        
def restaCarrito(request, producto_id):
    producto=ProductoCarrito.objects.get(id=producto_id)
    producto.resta()
    return redirect('homeCarrito')

@login_required
def sumaCarrito(request, producto_id):
    producto=ProductoCarrito.objects.get(id=producto_id)
    producto.suma()
    print(f'esta cantidad tiene el producto en el carrito {producto.cantidad}')
    return redirect("homeCarrito")

@login_required
def eliminar_del_carrito(request, producto_id):
    producto=ProductoCarrito.objects.get(id=producto_id)
    producto.eliminar()
    return redirect ('homeCarrito')


@login_required
# esta vista esta para comprar o agregar desde homeProducto
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
        

        
       
        form = PedidoForm(user=request.user, request=request)

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
            if request.user.groups.filter(name='administrador').exists():
                messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
                return redirect('homeProductos')
            else:
                messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
                return redirect('menu')
        # aqui se compra desde producto homeProducto
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
                restaExistencia = productoReal.existencia - cantidad_value
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
                    
                
            # #     #aqui comienza el bloque donde creamos una instancia de nuestro modelo pedido_producto
                    form=PedidoProductoForm()
                    pedidoProducto=form.save(commit=False)
                    pedidoProducto.pedido=pedido
                    pedidoProducto.producto=productoReal
                
                    pedidoProducto.cantidad=cantidad_value
            # #     #este atributo es de nuestro modelo Producto
            # #     productoCarrito.producto.disminuir(productoCarrito.cantidad)
            # #     #guardamos en la bd el producto o productos
                    if productoReal.tipo=='m':
                        pedido.save()
                        pedidoProducto.save()
                        if request.user.groups.filter(name='administrador').exists():
                            messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
                            return redirect('homeProductos')
                        else:
                            messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
                            return redirect('menu')
                        
                        
                    else:
                        if productoReal.existencia - cantidad_value >= 0:
                            productoReal.disminuir(cantidad_value)
                            pedido.save()
                            pedidoProducto.save()
                            if request.user.groups.filter(name='administrador').exists():
                                messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
                                return redirect('homeProductos')
                            else:
                                messages.success(request, f'{productoReal.nombre} se ha agregado al carrito.')
                                return redirect('menu')
                        else:
                            if request.user.groups.filter(name='administrador').exists():
                                messages.error(request, f'{productoReal.nombre} se ha agregado al carrito.')
                                return redirect('homeProductos')
                            else:
                                messages.error(request, f'{productoReal.nombre} se ha agregado al carrito.')
                                return redirect('menu')
                           
                            
            # 
                
            except Exception as e:
                    # Si ocurre un error, se captura y el usuario es redirigido
                    print(f"Error: {e}")
                    return redirect('homeProductos')
                
# este es el boton de comprar en el homeCarrito
@login_required
def comprar(request, producto_id=None, origen=None):
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
                
                
                #aqui comienza el bloque donde creamos una instancia de nuestro modelo pedido_producto
                form=PedidoProductoForm()
                pedidoProducto=form.save(commit=False)
                pedidoProducto.pedido=pedido
                pedidoProducto.producto=productoReal
                
                pedidoProducto.cantidad=productoCarrito.cantidad
                if productoReal.tipo=='m':
                        pedido.save()
                        pedidoProducto.save()
                        productoCarrito.eliminar()
                        messages.success(request, 'Compra exitosa, espere a que tomen su pedido')
                        return redirect('homeProductos')
                        
                        
                else:
                    if productoReal.existencia - productoCarrito.cantidad >= 0:
                            productoReal.disminuir(productoCarrito.cantidad)
                            pedido.save()
                            pedidoProducto.save()
                            productoCarrito.eliminar()
                            messages.success(request, 'Compra exitosa, espere a que tomen su pedido')
                            return redirect('homeProductos')
                    else:
                        messages.error(request, 'La cantidad seleccionada excede la existencia.')
                        return redirect('homeProductos')  # Ajusta según el nombre de tu URL para ProductosListaViews
                
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

#este es la logica para comprar en el formulario de home
def comprarfromhome(request):
    if request.method=='POST':
        pedidoform=PedidoForm(request.POST, user=request.user)
        pedidoproductoform=PedidoProductoForm(request.POST)
        
        try:
            if pedidoform.is_valid() and pedidoproductoform.is_valid():
                productoReal=pedidoproductoform.cleaned_data['producto']
                cantidad=pedidoproductoform.cleaned_data['cantidad']
                precio_total=cantidad * productoReal.precio
                print(f'esto es pedido{pedidoform} y esto el producto con la cantidad{pedidoproductoform}, esto es el precio total{precio_total}')
                pedido=pedidoform.save(commit=False)
                pedido.user = request.user
                pedido.precio_total = precio_total
                pedido.estatus = 'E'  # Estado "Espera"
                pedido.horario_entrega = now()
                
                pedidoproducto=pedidoproductoform.save(commit=False)
                pedidoproducto.pedido=pedido
                pedidoproducto.producto=productoReal
                pedidoproducto.cantidad=cantidad
                if productoReal.tipo=='m':
                    pedido.save()
                    pedidoproducto.save()
                    # productoCarrito.eliminar()
                    messages.success(request, 'Compra exitosa, espere a que tomen su pedido')
                    return redirect('home')
                            
                            
                else:
                    if productoReal.existencia - cantidad >= 0:
                        productoReal.disminuir(cantidad)
                        pedido.save()
                        pedidoproducto.save()
                            # productoCarrito.eliminar()
                        messages.success(request, 'Compra exitosa, espere a que tomen su pedido')
                        return redirect('home')
                    else:
                        messages.error(request, 'La cantidad seleccionada excede la existencia.')
                        return redirect('home')  # Ajusta según el nombre de tu URL para ProductosListaViews
        except:
            messages.error(request, 'algo salio mal, intente de nuevo.')
            return redirect('home')
            
#este es la logica para comprar todo el carrito            
def comprar_listacarrito(request):
    if request.method=='POST':
        
        accion = request.POST.get("accion")
          
        if accion=='comprar_todo':
            
            try:
                seleccionados = request.POST.getlist('seleccionados') 
                
                request.session['seleccionados'] = seleccionados
                print(f'Guardado en la sesión: {request.session["seleccionados"]}') 
                
                request.session.save()
                print(f'dentro de accion linea 340{seleccionados}')
                
                carrito=Carrito.objects.get(user=request.user) 
                
                
               
                subtotal=0.0
                carritoProductos=[]
                for producto_id in seleccionados:
                    print(producto_id)
                    producto=ProductoCarrito.objects.filter(carrito=carrito, id=int(producto_id))
                    print(f'esto trae {producto}')
                    for elemento in producto:
                        
                        total=float(elemento.cantidad) * float(elemento.precio_unitario)
                        subtotal+=total
                    # Agregar al carrito en formato de diccionario
                        carritoProductos.append({
                            'id': elemento.id,
                            'nombre': elemento.producto.nombre,  # Asegúrate de que este campo exista
                            'cantidad': int(elemento.cantidad),  # Convertir cantidad a entero
                            'precio_unitario': float(elemento.precio_unitario),  # Convertir a float
                            'total': float(total) 
                                    })
                    request.session['subtotal'] = float(subtotal)
                    request.session.save()
                
                    
                print(f'estos son los prodductos{carritoProductos}')
                
                
                    
            except:
                seleccionados=[]
                # carrito=None
                # carritoProductos=None
            
           

           
            form = PedidoForm(user=request.user)
            return render(request, 'carrito/compraCarrito.html', {
                    'form': form,
                    'productos':carritoProductos,
                    'subtotal':subtotal
                    
                })
        # proceso que hace que guarde los datos que queremos comprar
        else:
            seleccionados = [int(id) for id in request.session.get('seleccionados', [])]
            print(f'esto me trae seleccionados del else{seleccionados}')
            subtotal = Decimal(request.session.get('subtotal', 0))
            
            form=PedidoForm(request.POST, user=request.user)
            # print(f'esto trae el carrito{carritoProductos[1]['id']}')
        

            if form.is_valid():
                print(f'form ya validado')
                pedido=form.save(commit=False)
                pedido.user=request.user
                pedido.horario_entrega=now()
                pedido.estatus='p'
                pedido.precio_total=subtotal
                # pedido.save()
                print(f'esto trae el pedido preguardado{pedido}')
                try:
                    print('estra al try')
                    # print(f'Tipo de carritoProductos: {type(carritoProductos[1])}')
                    pedido.save()
                    for id in seleccionados:
                        
                        producto=ProductoCarrito.objects.get(id=id)
                        print(f'Elemento del carrito: {producto}, Tipo: {type(producto)}')
                        Pedido_Producto.objects.create(
                            pedido=pedido,
                            
                            producto=producto.producto,
                            
                            cantidad=producto.cantidad)
                        producto.producto.disminuir(producto.cantidad)
                        producto.eliminar()
                        
                    
                    messages.success(request, 'Compra exitosa, espere a que tomen su pedido')
                    return redirect('homeCarrito')
                    
                except Exception as e:
                    print('entre al except')
                    # Si ocurre un error, imprime o maneja el mensaje
                    print(f"Error al procesar el pedido: {e}")
                    # Opcionalmente, podrías realizar un rollback o limpiar objetos creados
                    # pedido.delete()
                    messages.error(request, 'No se pudo guardar su pedido, intente de nuevo.')
                    return redirect('homeCarrito')
                    # Si es necesario, elimina el pedido creado
                    
                    
            # datos={
                
            # }
            # Pedido_Producto.objects.create(**datos)
    
                
                

        
      
            
def historial(request):
    pedidos = Pedido.objects.prefetch_related('productos').filter(user=request.user)
    return render (request, 'historial/historial.html', context={'pedidos':pedidos})
           
        