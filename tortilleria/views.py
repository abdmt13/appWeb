from django.shortcuts import render, redirect
from carrito.models import Pedido, PedidoRepartidor
from .models import Informacion_Tortilleria, HistorialEmpleado
from django.contrib.auth.models import Group, User
from .forms import InformacionTortilleriaForm, AsignarEmpleadoForm, SeleccionaRepartidorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def verificarGrupo(request):
    pass
    # usuario = request.user  # Asegúrate de que request['id'] existe
    # if usuario.groups.filter(name='administrador').exists() or usuario.is_superuser:
    #     return redirect('homeTortilleria')
    # elif usuario.groups.filter(name='repartidor').exists():
    #     return redirect('homeTortilleriaRepartidor')



@login_required
def homeTortilleriaAdmin(request):
    if request.method =='GET':
        clave_sesion = f'pedidosRepartidor_{request.user.id}'
        print (clave_sesion)
        print("Claves en la sesión:", request.session.keys())

        pedidos = Pedido.objects.prefetch_related('productos').filter(estatus='E')
        return render (request, 'home_tortilleria.html', context={'pedidos': pedidos})
    # else:

def homeTortilleriaRepartidor(request):
    
    clave_sesion = f'pedidosRepartidor_{request.user.id}'
    print (clave_sesion)
    print("Claves en la sesión:", request.session.keys())


    id_pedidos = request.session.get(clave_sesion, [])
    print(id_pedidos)
    listaPedido=[]
    for id in id_pedidos:
        pedido=Pedido.objects.get(id=id)
        listaPedido.append(pedido)


    print(f'Esto trae id_pedidos: {listaPedido}')
    return render (request, 'homeTortilleriaRepartidor.html')
    

@login_required
def seleccionarAccion(request): 
    if request.method == 'POST':
        accion = request.POST.get('accion')
        id_pedido = request.POST.getlist('seleccionados')
        noPedidos = len(id_pedido)
        if accion == 'repartidor':
            try:
                if noPedidos == 0:
                    messages.error(request, 'No se seleccionó ningún pedido')
                    return redirect('homeTortilleria')
                else:
                    request.session['pedidosRepartidor'] = id_pedido
                    # request.session['pedidosLista'] = id_pedido
                    print(f'Guardado en la sesión repartidor: {request.session["pedidosRepartidor"]}') 
                    
                    
                    request.session.save()
                    
            except: 
                messages.error(request, 'Error al obtener el pedido')
                return redirect('homeTortilleria')

            form=SeleccionaRepartidorForm()
            return render(request, 'forms/seleccionaRepartidor.html', context={'form':form})

            print('Enviando al Repartidor')
          
        elif accion=='lista':
            print('Acción lista')
        else:
            form=SeleccionaRepartidorForm(request.POST)
            if form.is_valid():
                repartidor=form.cleaned_data['empleado']
                pedidorepartidor=PedidoRepartidor()
                pedidorepartidor.repartidor=repartidor.usuario
                pedidos=request.session.get('pedidosRepartidor', None)
                # clave_sesion = f'pedidosRepartidor_{repartidor.usuario.id}'
                # print(clave_sesion)
                # request.session[clave_sesion] = request.session.get('pedidosRepartidor', None)
                # request.session.modified = True
                # request.session.save()
                diccionario={}
                for idpedido in pedidos:
                    pedido=Pedido.objects.get(id=idpedido)
                    pedido.estatus='C'
                    pedido.save()
                    diccionario= {
                        'id': pedido.id,
                        'nombre': pedido.nombre,  # Asegúrate de que tiene un campo "nombre"
                        'estatus': pedido.estatus,
                        'precio': pedido.precio,  # Agrega más campos según tu modelo
                    }
                pedidorepartidor.pedidos=diccionario
                pedidorepartidor.save()
                messages.success(request, f'Pedidos enviados al repartidor{repartidor}')
                # print(F'esto me trae la sesion{request.session[f'pedidosRepartidor{repartidor}']}')
                return redirect('homeTortilleriaAdmin')
            


# funcion para guardar la informacion de la tortilleria
@login_required
def informacionTortilleria(request):
    if request.method == 'POST':
        info=Informacion_Tortilleria.objects.all().count()
        if info < 1:
            form = InformacionTortilleriaForm(request.POST, request.FILES)
            
            
        else: 
            print(f'este es el tipo{type(info)} y esto el numero {info}')
            # info=Informacion_Tortilleria.objects.all().count()
            # id_tor=info
            # print(type(info))
            informacion=Informacion_Tortilleria.objects.last()
            
            form = InformacionTortilleriaForm(request.POST, request.FILES, instance=informacion)  # Maneja archivos con request.FILES
            
            
        if form.is_valid():
            form.save()
            return redirect('informacionTortilleria')  # Cambia por la ruta a la que quieras redirigir
    else:
       
        try:
            informacion = Informacion_Tortilleria.objects.last()  # Obtiene el último registro
            if informacion:
                form = InformacionTortilleriaForm(instance=informacion)
            else:
                form = InformacionTortilleriaForm()  # Si no hay registros, crea un formulario vacío
        except Exception as e:
            print(f"Error: {e}")  # Imprime el error para depuración
            informacion = None
            form = InformacionTortilleriaForm()  # Asegura que 'form' tenga un valor

        return render(request, 'informacion/informacion_tortilleria.html', {'form': form, 'informacion': informacion})

def guardarEmpleado(request):
    if request.method == 'POST':
        form = AsignarEmpleadoForm(request.POST)
        if form.is_valid():
            grupo = form.cleaned_data['grupo']
            usuario = form.cleaned_data['usuario']
            usuario.groups.add(grupo)  # Asigna el usuario al grupo
            HistorialEmpleado.objects.create(usuario=usuario, grupo=grupo)
            messages.success(request, f'Usuario {usuario.username} agregado a {grupo.name}')
            return redirect('guardarEmpleado')  # Recarga la página después de guardar
    else:
        form = AsignarEmpleadoForm()
        empleados = HistorialEmpleado.objects.all()

        # grupos = Group.objects.all()
        # usuarios = User.objects.all()
        
        return render(request, 'informacion/empleados.html', context={
            'form': form,
            'empleados': empleados,
        })
    
def eliminarEmpleado(request, id_empleado):
    try: 
        empleado=HistorialEmpleado.objects.get(id=id_empleado)
        print(f'este es el empleado {empleado} y este su grupo{empleado.grupo}')
        
        empleado.eliminar()
        # empleado.usuario.groups.remove(empleado.grupo)  #  Eliminar el usuario del grupo
        messages.success(request, f'Usuario {empleado.usuario.first_name} {empleado.usuario.last_name} descativado')
        print('eliminando')

        return redirect('guardarEmpleado')

    
    except:
        print('no se pudo eliminar')
        messages.error(request, f'No se pudo eliminar al usuario')
            
        return redirect('guardarEmpleado')  # Redirigir después de eliminar
    # return render(request, 'empleados.html')

def activarEmpleado(request, id_empleado):
    empleado=HistorialEmpleado.objects.get(id=id_empleado)
    empleado.activar()
    messages.success(request, f'Usuario {empleado.usuario.first_name} {empleado.usuario.last_name} activado ')
        # print('eliminando')
    return redirect ('guardarEmpleado')
