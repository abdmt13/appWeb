from django.urls import path

from . import views
from .views import ProductosListaViews

urlpatterns = [
    path("",views.homeCarrito, name='homeCarrito'),
    path("menu", ProductosListaViews.as_view(), name='menu'),
    path("gestionarAccion/<int:producto_id>/", views.gestionarAccion, name="gestionarAccion"), 
    path("restaCarrito/<int:producto_id>/", views.restaCarrito, name="restaCarrito"),
    path("sumaCarrito/<int:producto_id>/", views.sumaCarrito, name="sumaCarrito"),
    path('comprar/<int:producto_id>/<str:origen>/', views.comprar, name="comprar"),
    path("eliminar_del_carrito/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    
    
    # path('cobro_en_tienda', views.cobroEnTienda, name='cobroEnTienda'),
    
]