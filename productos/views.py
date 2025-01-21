from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import productoForm, BuscarProductoForm, AgregarInventarioForm, CantidadForm
from .models import Producto
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def in_group_administradores(user):
    
    return user.groups.filter(name='admi').exists()




# este es mi home, de aqui se imprimen todos los datos del producto

class ProductosListaViews(LoginRequiredMixin, ListView):
    model=Producto
    template_name = 'vistasProducto/verProducto.html'  # Tu plantilla
    context_object_name = 'productos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formCantidad']=CantidadForm()
        # context['form'] = BuscarProductoForm()  # Agrega el formulario al contexto
        
        return context
    
    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         return Producto.objects.filter(nombre__icontains=query)
    #     return Producto.objects.all()
# Create your views here.
# def homeProductos(request):
#     form=BuscarProductoForm
#     productos=Producto.objects.all()
    
#     return render(request, 'vistasProducto/verProducto.html', context={'productos':productos, 'form':form} )

@user_passes_test(in_group_administradores)
@login_required
def agregarProducto(request):
    if request.method =="GET":
        form=productoForm
        return render (request, 'vistasProducto/crearProducto.html', context={'form':form})
    else:
        
        try:
            form=productoForm(request.POST)
            if form.is_valid():
                # print(form)
                producto=form.save(commit=False)
                
                producto.save()
                return redirect('homeProductos')
        except:
            return render(request, 'vistasProducto/crearProducto.html', context={'form':form, 'error':'Algo ah salido mal, intente de nuevo'})
        
@login_required     
def editarProducto(request, id):
    if request.method=="GET":
        producto=Producto.objects.get(id=id)
        form=productoForm(instance=producto)
        return render(request, 'vistasProducto/crearProducto.html', context={'form':form})
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
@login_required        
def buscarProducto(request):
    if request.method=='GET':
        formProducto=BuscarProductoForm
        return render(request, 'vistasProducto/inventario/ajuste_inventario.html', context={'formProducto':formProducto})
    else:
        producto=[]
        accion = request.POST.get('action')
        if accion =='buscar':
            formProducto=BuscarProductoForm(request.POST)
            if formProducto.is_valid():
                codigo=formProducto.cleaned_data['codigo']
                try:
                    producto=Producto.objects.get(codigo=codigo)
                    formInventario=AgregarInventarioForm
                    print(producto)
                    return render(request, 'vistasProducto/inventario/ajuste_inventario.html', { 'producto': producto, 'formInventario':formInventario})
                except Producto.DoesNotExist:
                    return render(request, 'vistasProducto/inventario/ajuste_inventario.html', {'form': formProducto, 'error': 'Producto no encontrado.'})
        
            
@login_required                   
def ajusteInventario(request, producto_id):
    if request.method=='POST':
        formInventario = AgregarInventarioForm(request.POST)
        producto=Producto.objects.get(id=producto_id)
        if formInventario.is_valid():
            try:
                existencia = formInventario.cleaned_data['existencia']
                print(f'esto es la existencia: {existencia}')
                if existencia > 0:
                    producto.incrementar(existencia)  # Incrementa la existencia
                else:
                    producto.disminuir(abs(existencia))  # Disminuye la existencia
                return redirect('homeProductos')
            except Exception as e:
                print(f"Error: {e}")  # Imprime el error para depurar
                return redirect('buscarProducto')

        # try:
        #     producto=Producto.objects.get(id=producto_id)
        #     print(producto)
        #     formInventario=AgregarInventarioForm(request.POST)
        #     existencia=formInventario.cleaned_data['existencia']
            
        #     if formInventario.is_valid():
        #         print(f'esto trae el form{formInventario['existencia']} y este es el prodyucto que queremos modificar{producto}')
                
        #         print(f'esto es la existencia:{existencia}')
        #         if existencia > 0:
        #             producto.incrementar(producto, existencia)
        #         else:
        #             producto.disminuir(abs(existencia))
                
        #         return redirect('homeProducto')
                    
            
        # except:
        #     return redirect('buscarProducto')
                  
                
            
        
        
            
# def verProducto(request):
#     productos=Producto.objects.all()
#     # datos_sesion = request.session.items()

#     # Imprimir los datos
#     # for clave, valor in datos_sesion:
#     #     print(f"esto trae el request:{clave}: {valor}")
#     return render(request, 'vistasProducto/producto/verProducto.html', context={'productos':productos} )