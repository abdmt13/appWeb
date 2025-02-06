from django.contrib.auth.models import Group
from tortilleria.models import Informacion_Tortilleria

def permisos_globales(request):
    if request.user.is_authenticated:  # Solo para usuarios autenticados
        permiso = request.user.groups.filter(name='administrador').exists()
        super_user = request.user.is_superuser
        return {
            'permiso': permiso,
            'super_user': super_user,
        }
    return {}



def informacion_tortilleria(request):
    informacion=Informacion_Tortilleria.objects.last()
    if informacion:
        return {'informacion': informacion}
    else:
        informacion = {
            "nombre": "Tortillería no disponible",
            "direccion": "No registrada",
            "horaInicio": "00:00",
            "horaFinal": "00:00",
            "imagen": None
        }
        return{'informacion': informacion}
    
    