from django.urls import path

from . import views
# from .views import 

urlpatterns = [
    path("",views.homeTortilleria, name='homeTortilleria'),
    
    path('informacion_totilleria', views.informacionTortilleria, name='informacionTortilleria'),
    path('acciones/', views.seleccionarAccion, name='seleccionarAccion'),





    # las url de abajo pertenecen a la seccion informacion de la tortileria
    path('guardarEmpleado/', views.guardarEmpleado, name='guardarEmpleado'),
    
    
    
    
    ]