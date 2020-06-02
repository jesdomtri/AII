# -*- encoding: utf-8 -*-
from django import forms
from main.models import Anime

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')
    
def get_lista():    
    valores = Anime.objects.values('generos').distinct()
    lista = []
    for v in valores:
        for v2 in v.values():
            v3 = v2.split(',')
            for v4 in v3:
                if v4 not in lista:
                    lista.append(v4.lstrip().strip())
    res = []
    id = 0
    for x in set(lista):
        res.append((x, x))
        id += 1
    return res

class BusquedaPorGeneroForm(forms.Form):
    genero = forms.ChoiceField(label="Seleccione el genero", choices=get_lista())