from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registroUser/",views.registroUser, name="registroUser"),
    path("iniciarSesionUser/", views.iniciarSesionUser, name="iniciarSesionUser"),
    path("closeUser/", views.closeUser, name="closeUser"),
    path("home/", views.home, name="home")
]