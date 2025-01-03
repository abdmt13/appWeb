from django.urls import path

from . import views

urlpatterns = [
    path("",views.homeCarrito, name='homeCarrito'),
    path("agregarCarrito/<int:producto_id>/", views.agregarCarrito, name="agregarCarrito"), 
    path("restaCarrito/<int:producto_id>/", views.restaCarrito, name="restaCarrito"),
    path("sumaCarrito/<int:producto_id>/", views.sumaCarrito, name="sumaCarrito"),
    # path("comprar/<int:producto_id>/", views.comprar, name="comprar"),
    path("eliminar_del_carrito/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    
]