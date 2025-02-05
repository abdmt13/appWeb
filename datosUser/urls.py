from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/",views.home, name='home'),
    path("registroUser/",views.registroUser, name="registroUser"),
    path("iniciarSesionUser/", views.iniciarSesionUser, name="iniciarSesionUser"),
    path("closeUser/", views.closeUser, name="closeUser"),
    
    path("homePerfil/", views.homePerfil, name="homePerfil"),
    path("nuevodomicilio/", views.nuevoDomicilio, name="nuevoDomicilio"),
    path("editarDomicilio/<int:id>/", views.editarDomicilio, name='editarDomicilio'),
    
    
    path("registroDatosPersonales/", views.registroDatosPersonales, name="registroDatosPersonales"),
    path("mis_pedidos/", views.mis_pedidos, name='mis_pedidos'),
    path('cancelar_pedido/<int:pedido_id>', views.cancelar_pedido, name='cancelar_pedido')
]