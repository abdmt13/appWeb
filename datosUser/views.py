from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import datosPersonalesForm, domicilioForm
from carrito.forms import PedidoForm, PedidoProductoForm
from .models import Domicilio
from carrito.models import Pedido, Pedido_Producto



def index(request):
    return render(request, 'index.html')
@login_required
def home(request):
    if request.method =='GET':
        pedidoform=PedidoForm(user=request.user)
        pedidoproductoform=PedidoProductoForm()
        permiso = request.user.groups.filter(name='admi').exists()  # Verifica si el usuario está en el grupo 'admi'
        super_user = request.user.is_superuser 
        # {'permiso': permiso,'super_user': super_user}
        return render(request, 'home.html', context={'pedidoform':pedidoform, 'pedidoproductoform':pedidoproductoform})
#  esta funcion registra al usuario y lo autentica de una vez

def registroUser(request):
    
    if request.method == 'GET':
        print('enviando formulario')
        return render (request, 'registro_user/registroUser.html',{
                'form': UserCreationForm
            })
        
    else:
        print(request.POST)
        print('obteniendo datos')
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                
                print(user)
                return redirect ('registroDatosPersonales')
                
            except IntegrityError:
                return render (request, 'registroUser.html',{
                'form': UserCreationForm,
                'error': 'username already exist'
                    })
        return render (request, 'registroUser.html',{
                'form': UserCreationForm,
                'error': 'password do not match'
                    })
       
    # return HttpResponse('hola como estas')

def iniciarSesionUser(request):
    if request.method == 'GET':
        return render (request, 'registro_user/iniciar_sesion.html', 
            {'form': AuthenticationForm})
    else:
        user= authenticate(request, username=request.POST['username'],
                           password=request.POST['password'])
        print(user)
        if user is None:
            return render (request, 'registro_user/iniciar_sesion.html', 
            {'form': AuthenticationForm,
             'error': 'el usuario o la contraseña son incorrectos'})
        else:
            # valor=request.session.get['firt_name']
            # print(f'esto es lo que trae el request{valor}')
            login(request,user)
            return(redirect('home'))
        
        
def closeUser(request):
    
    logout(request)
    return redirect('index')

@login_required

def homePerfil(request):
    
    domicilios=Domicilio.objects.filter(user=request.user)
    print(f'esto es  lo que trae domicilios {domicilios}')
    return render(request, 'vistaApp/homePerfil.html', context={'domicilios':domicilios})

@login_required
def registroDatosPersonales(request):
     # Obtener el usuario actual
    user = request.user
    nombre_vacio = not user.first_name.strip()  # Verifica si está vacío o solo espacios
    apellido_vacio = not user.last_name.strip()  # Verifica si está vacío o solo espacios

    
    

    if request.method == 'POST':
        form = datosPersonalesForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('homePerfil')  # Cambia 'perfil' por la URL deseada  
    else:
        form = datosPersonalesForm(instance=user)
        return render(request, 'vistaApp/datosPersonales/registroDatos.html', {'form': form, 'nombre':nombre_vacio, 'apellidos':apellido_vacio})

@login_required
def nuevoDomicilio(request):
    numeroDomicilio=Domicilio.objects.filter(user=request.user).count()
    print(f'este es el numero de domicilio {numeroDomicilio}')
    if numeroDomicilio==3:
        return render(request,'vistaApp/domicilios/nuevoDomicilio.html', context={'mensaje':True} ) 
        
    
    
    
    if request.method=="GET":
        form = domicilioForm(user=request.user)
        return render(request,'vistaApp/domicilios/nuevoDomicilio.html', context={'form':form, 'numeroDomicilio':numeroDomicilio} )  
    else:
        try:
            form=domicilioForm(request.POST)
            print(f'esto trae el {form}')
            if form.is_valid():
                domicilio = form.save(commit=False)
                domicilio.user = request.user
                domicilio.save()
                return redirect(homePerfil)
        except:
            form = domicilioForm(user=request.user)
            return render(request,'vistaApp/domicilios/nuevoDomicilio.html', context={'form':form} ) 

@login_required           
def editarDomicilio(request, id):
    if request.method=="GET":
        domicilio=Domicilio.objects.get(user=request.user, id=id)
        print(F'esto es lo que trae el domicilio: {domicilio}')
        form=domicilioForm(instance=domicilio)
        return render(request, 'vistaApp/domicilios/editDomicilio.html', context={'form':form})
        
    else:
        try:
            domicilio=Domicilio.objects.get(user=request.user, id=id)
            form=domicilioForm(request.POST, instance=domicilio)
            if form.is_valid():
                    domicilio = form.save(commit=False)
                    domicilio.user = request.user
                    domicilio.save()
                    return redirect(homePerfil)
        except:
            form = domicilioForm(user=request.user)
            return render(request,'vistaApp/domicilios/nuevoDomicilio.html', context={'form':form, 'error':'algo salio mal'} ) 
        
        
        
def mis_pedidos(request):
    pedido=Pedido.objects.filter(user=request.user).filter(estatus='E')
    # pedidopedidos = Pedido.objects.prefetch_related('productos').filter(user=request.user).filter(estatus='E')
    # print(pedidopedidos)
    return render(request, 'vistaApp/datosPersonales/mis_pedidos.html', context={'pedidopedidos':pedido})

def cancelar_pedido(request, pedido_id):
    pedido=Pedido.objects.get(id=pedido_id)
    print(f'esto es el pedido: {pedido}')
    pedido.estatus='X'
    pedido.save()
    return redirect(mis_pedidos)
    
    