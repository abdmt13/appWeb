from django.urls import path

from . import views

urlpatterns = [
    path("",views.homeCarrito, name='homeCarrito'),
    path("agregarCarrito/<int:producto_id>/", views.agregarCarrito, name="agregarCarrito")
    
]