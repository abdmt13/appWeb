from django.urls import path

from . import views

urlpatterns = [
    path("",views.homeProductos, name='homeProductos'),
    
]