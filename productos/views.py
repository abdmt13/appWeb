from django.shortcuts import render, redirect
from .forms import productoForm
from .models import Producto
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

def in_group_administradores(user):
    return user.groups.filter(name='admin').exists()






# Create your views here.
def homeProductos(request):
    return render (request, 'homeproductos.html')

@user_passes_test(in_group_administradores)
def agregarProducto(request):
    if request.method =="GET":
        form=productoForm
        return render (request, 'vistasProducto/producto/crearProducto.html', context={'form':form})
    else:
        
        try:
            form=productoForm(request.POST)
            if form.is_valid:
                print(form)
                producto=form.save(commit=False)
                producto.save()
                return redirect(homeProductos)
        except:
            return render(request, 'vistasProducto/producto/crearProducto.html', context={'form':form, 'error':'Algo ah salido mal, intente de nuevo'})
        
      
def editarProducto(request, id):
    if request.method=="GET":
        producto=Producto.objects.get(id=id)
        form=productoForm(instance=producto)
        return render(request, 'vistasProducto/producto/crearProducto.html', context={'form':form})
    else:
        try:
            producto=Producto.objects.get(id=id)
            form=productoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                print(f"esto es lo que debe de guardar el form:{form}")
                return redirect('verProducto')
        except:
            print(f"algo ha salido mal con el form")
        
        
def verProducto(request):
    productos=Producto.objects.all()
    datos_sesion = request.session.items()

    # Imprimir los datos
    for clave, valor in datos_sesion:
        print(f"esto trae el request:{clave}: {valor}")
    return render(request, 'vistasProducto/producto/verProducto.html', context={'productos':productos} )