from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registroUser/",views.registroUser, name="registroUser"),
    path("iniciarSesionUser/", views.iniciarSesionUser, name="iniciarSesionUser"),
    path("closeUser/", views.closeUser, name="closeUser"),
    
    path("homePerfil/", views.homePerfil, name="homePerfil"),
    path("nuevodomicilio/", views.nuevoDomicilio, name="nuevoDomicilio"),
    
    
    
    path("registroDatosPersonales/", views.registroDatosPersonales, name="registroDatosPersonales")
]