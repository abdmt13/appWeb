from django.shortcuts import render, redirect
from carrito.models import Pedido
from .models import Informacion_Tortilleria, HistorialEmpleado
from django.contrib.auth.models import Group, User
from .forms import InformacionTortilleriaForm, AsignarEmpleadoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homeTortilleria(request):
    if request.method =='GET':
    # Obtener pedidos y productos relacionados
        pedidos = Pedido.objects.prefetch_related('productos').filter(estatus='E')
        return render (request, 'home_tortilleria.html', context={'pedidos': pedidos})
    # else:

@login_required
def seleccionarAccion(request): 
    if request.method == 'POST':
        try:
            id_pedido = request.POST.getlist('seleccionados')
            noPedidos = len(id_pedido)
            if noPedidos == 0:
                messages.error(request, 'No se seleccionó ningún pedido')
                return redirect('homeTortilleria')
            else:
                request.session['pedidosRepartidor'] = id_pedido
                request.session['pedidosLista'] = id_pedido
                print(f'Guardado en la sesión repartidor: {request.session["pedidosRepartidor"]} guardado en la sesión lista: {request.session["pedidosLista"]}') 
                
                
                request.session.save()
                
        except: 
            messages.error(request, 'Error al obtener el pedido')
            return redirect('homeTortilleria')
        accion = request.POST.get('accion')
        if accion == 'repartidor':

            print('Enviando al Repartidor')
            # id_pedido = request.POST.get('id_pedido')
            # pedido = Pedido.objects.get(id=id_pedido)
            # pedido.estatus = 'E'
        else:
            print('Acción lista')


 
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
        
        empleado.estatus=False
        empleado.save()
        empleado.usuario.groups.remove(empleado.grupo)  #  Eliminar el usuario del grupo
        messages.success(request, f'Usuario {empleado.usuario.first_name} {empleado.usuario.last_name} eliminado del grupo {empleado.grupo}')
        print('eliminando')

        return redirect('guardarEmpleado')

    
    except:
        print('no se pudo eliminar')
        messages.error(request, f'No se pudo eliminar al usuario')
            
        return redirect('guardarEmpleado')  # Redirigir después de eliminar
    # return render(request, 'empleados.html')
