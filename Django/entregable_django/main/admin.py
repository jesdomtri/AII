from django.contrib import admin
from main.models import Noticia, Autor, Fuente

#registramos en el administrador de django los modelos 
admin.site.register(Fuente)
admin.site.register(Autor)
admin.site.register(Noticia)