from django.shortcuts import render 

# Create your views here.
def homeProductos(request):
    return render (request, 'homeproductos.html')