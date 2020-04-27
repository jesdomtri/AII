#encoding:utf-8
from principal.models import Receta, Comentario
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings

#muestra una pantalla con el t�tulo del proyecto. Es un ahtml est�tico
def sobre(request):
    html="<html><body>Proyecto de ejemplo de vistas</body></htm>"
    return HttpResponse(html)

#muestra los t�tulos de las recetas que est�n registradas
def inicio(request):
    recetas=Receta.objects.all()
    return render(request,'inicio.html', {'recetas':recetas})

#muestra los datos de los usuarios y las recetas que han registrado
def usuarios(request):
    recetas=Receta.objects.all()
    usuarios=User.objects.all()
    return render(request,'usuarios.html', {'recetas':recetas,'usuarios':usuarios})

#muestra el t�tulo de las recetas registradas (con un enlace a detalle de la misma) y una foto
def lista_recetas(request):
    recetas=Receta.objects.all()
    return render(request,'recetas.html', {'datos':recetas,'MEDIA_URL': settings.MEDIA_URL})

#muestra detalles de una receta (ingredientes, preparaci�n y comentarios de los usuarios)
def detalle_receta(request, id_receta):
    dato = get_object_or_404(Receta, pk=id_receta)
    comentarios=Comentario.objects.filter(receta=id_receta)
    return render(request,'receta.html',{'receta':dato, 'comentarios':comentarios,'MEDIA_URL': settings.MEDIA_URL})