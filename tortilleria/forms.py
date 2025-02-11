from django import forms
from .models import Informacion_Tortilleria
from django.contrib.auth.models import Group, User
# from datosUser.models import DatosUser

# formulario para guardar la informacion de la tortilleria
class InformacionTortilleriaForm(forms.ModelForm):
    class Meta:
        model = Informacion_Tortilleria
        fields = ['nombre', 'direccion', 'horaInicio', 'horaFinal', 'imagen']  # Incluye el campo de imagen

# formulario para asignar un usuario a un grupo
class AsignarEmpleadoForm(forms.Form):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grupo")
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Usuario",
        widget=forms.Select()
    )

    def __init__(self, *args, **kwargs):
        super(AsignarEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.all()
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} ({obj.username})"