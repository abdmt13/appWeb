from django.contrib.auth.models import Group

def permisos_globales(request):
    if request.user.is_authenticated:  # Solo para usuarios autenticados
        permiso = request.user.groups.filter(name='admi').exists()
        super_user = request.user.is_superuser
        return {
            'permiso': permiso,
            'super_user': super_user,
        }
    return {}
