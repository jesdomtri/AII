#encoding:utf-8
from django import forms
from main.models import Noticia
    
class BusquedaPorContenidoForm(forms.Form):
    contenido = forms.CharField(label='Palabra en el contenido', widget=forms.TextInput(), required=True)