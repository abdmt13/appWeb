from django.urls import path

from . import views

urlpatterns = [
    path("",views.homeProductos, name='homeProductos'),
    path("agregarProducto/", views.agregarProducto, name='agregarProducto'),
    path("verproducto/", views.verProducto, name='verProducto'),
    path("editarproducto/<int:id>/", views.editarProducto, name='editarProducto')
    
]