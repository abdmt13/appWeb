from django.urls import path

from . import views
# from .views import 

urlpatterns = [
    path("",views.homeTortilleria, name='homeTortilleria'),
    
    path('informacion_totilleria', views.informacionTortilleria, name='informacionTortilleria'),
    
    
    
    
    ]