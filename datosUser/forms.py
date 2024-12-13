from django import forms
from django.forms import modelformset_factory
from django.forms import ModelForm
from .models import Domicilio
from django.contrib.auth.models import User



class datosPersonalesForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email']
        
        

# class domicilioForm(ModelForm):
#     class Meta:
#         model=Domicilio
#         field=['nombrecompleto', 'calle', 'entreCalle']        