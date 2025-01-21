from django.shortcuts import render
from carrito.models import Pedido

# Create your views here.
def homeTortilleria(request):
    # Obtener pedidos y productos relacionados
    pedidos = Pedido.objects.prefetch_related('productos')
    return render (request, 'home_tortilleria.html', context={'pedidos': pedidos})