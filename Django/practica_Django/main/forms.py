#encoding:utf-8
from django import forms
from main.models import Uva
   
class BusquedaPorUvaForm(forms.Form):
    lista=[(g.id,g.nombre) for g in Uva.objects.all()]
    uva = forms.ChoiceField(label="Seleccione la uva", choices=lista)