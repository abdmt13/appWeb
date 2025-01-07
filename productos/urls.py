from django.urls import path

from . import views

urlpatterns = [
    path("",views.homeProductos, name='homeProductos'), #en esta url aparecen todos los productos
    path("agregarProducto/", views.agregarProducto, name='agregarProducto'),
    # path("verproducto/", views.verProducto, name='verProducto'),
    path("editarproducto/<int:id>/", views.editarProducto, name='editarProducto'),
    
    
     path("ajusteInventario/<int:producto_id>/", views.ajusteInventario, name='ajusteInventario'),
     path("buscarProducto/", views.buscarProducto, name='buscarProducto'),
    # path("/"),
    
    # pvc y cpv, en la taza de baño asunque no le baje filtra el agua
    # el lababo no sale el agua pero esta todo oxidado y roto
    
]