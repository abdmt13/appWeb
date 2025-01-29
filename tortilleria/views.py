from django.shortcuts import render, redirect
from carrito.models import Pedido
from .models import Informacion_Tortilleria
from .forms import InformacionTortilleriaForm
from django.contrib import messages

# Create your views here.
def homeTortilleria(request):
    # Obtener pedidos y productos relacionados
    pedidos = Pedido.objects.prefetch_related('productos')
    return render (request, 'home_tortilleria.html', context={'pedidos': pedidos})





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

