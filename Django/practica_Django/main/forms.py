#encoding:utf-8
from django import forms
from main.models import Uva
   
class BusquedaPorUvaForm(forms.Form):
    uva = forms.ModelChoiceField(label="Seleccione la uva", queryset=Uva.objects.all())