from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import datosPersonalesForm



def index(request):
    return render(request, 'index.html')

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
            login(request,user)
            return(redirect('homePerfil'))
        
        
def closeUser(request):
    
    logout(request)
    return redirect('index')

@login_required
def homePerfil(request):
    return render(request, 'vistaApp/homePerfil.html')

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

def nuevoDomicilio(request):
    # if request.method=="GET":
    #     return render(request,'vistaApp/domicilios/nuevoDomicilio' context={'form':} )   
    pass       