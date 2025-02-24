from django.urls import path

from . import views
# from .views import 

urlpatterns = [
    path("",views.homeTortilleriaAdmin, name='homeTortilleriaAdmin'),#para el administrador
    path('homeTortilleriaRepartidor', views.homeTortilleriaRepartidor, name='homeTortilleriaRepartidor'),
    # path('homeTortilleriaAdmin', views.homeTortilleria, name='homeTortilleria'),
    
    path('informacion_totilleria', views.informacionTortilleria, name='informacionTortilleria'),
    path('acciones/', views.seleccionarAccion, name='seleccionarAccion'),





    # las url de abajo pertenecen a la seccion informacion de la tortileria
    path('guardarEmpleado/', views.guardarEmpleado, name='guardarEmpleado'),
    path('eliminarEmpleado/<int:id_empleado>/', views.eliminarEmpleado, name='eliminarEmpleado'),
    path('activarEmpleado/<int:id_empleado>/', views.activarEmpleado, name='activarEmpleado'),
    
    
    
    
    ]