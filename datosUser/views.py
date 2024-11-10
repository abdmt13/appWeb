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
                return redirect ('home')
                
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
            return(redirect('home'))
        
        
def closeUser(request):
    
    logout(request)
    return redirect('index')

@login_required
def home(request):
    return render(request, 'home.html')

def registroDatosPersonales(request):
    return render (request, "vistaApp/datosPersonales/registroDatos.html")