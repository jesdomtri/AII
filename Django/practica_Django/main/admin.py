from django.contrib import admin
from main.models import Uva, Denominacion, Bodega, Vino

#registramos en el administrador de django los modelos 
admin.site.register(Uva)
admin.site.register(Denominacion)
admin.site.register(Bodega)
admin.site.register(Vino)