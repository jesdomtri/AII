#encoding:utf-8
from main.models import Autor, Fuente, Noticia
from main.forms import BusquedaPorContenidoForm
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib.request
import lxml
import re
from datetime import datetime

def cargaBD():
    num_noticias = 0

    Autor.objects.all().delete()
    Fuente.objects.all().delete()
    Noticia.objects.all().delete()

    lista = []

    url = urllib.request.urlopen("https://www.meneame.net/")
    bs = BeautifulSoup(url, "lxml")
    lista_noticias = bs.find_all("div", class_="center-content")
    lista_comentarios = bs.find_all("div", class_="news-details")
    for i in lista_noticias:
        titulo = i.h2.a.string
        aux = i.find("div", class_="news-submitted")
        autor = aux.find_all("a")[1].string      
        fuentelink = aux.find("span", class_="showmytitle")
        if fuentelink:
            fuente = fuentelink.string
            link = fuentelink['title']
        else:
            fuente = "Anonima"
            link = "Desconocido"
        if aux.find("span", {'data-ts':True, 'title':re.compile("publicado")}): 
            fecha_ts = aux.find("span", {'data-ts':True, 'title':re.compile("publicado")})['data-ts']
        else: 
            fecha_ts = aux.find("span", {'data-ts':True, 'title':re.compile("enviado")})['data-ts']
        fecha = datetime.fromtimestamp(int(fecha_ts))
        contenido = i.find("div", class_="news-content").get_text() 
        num_comentarios = int(lista_comentarios[lista_noticias.index(i)].find('a', class_="comments").get("data-comments-number"))
        lista.append((titulo, autor, fuente, link, fecha, contenido,num_comentarios))


        autor_obj, creado = Autor.objects.get_or_create(nombre=autor)
        fuente_obj, creado = Fuente.objects.get_or_create(nombre=fuente)
        Noticia.objects.create(titulo = titulo, autor = autor_obj,
                                fecha = fecha,
                                fuente = fuente_obj,                               
                                contenido = contenido,
                                num_comentarios = num_comentarios)
        num_noticias = num_noticias + 1

    return(num_noticias)
        
def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_noticias = cargaBD()
            mensaje="Se han almacenado: " + str(num_noticias) + " noticias"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def inicio(request):
    num_noticias=Noticia.objects.all().count()
    return render(request,'inicio.html', {'num_noticias':num_noticias})

def lista_noticias(request):
    noticias=Noticia.objects.all()
    return render(request,'noticias.html', {'noticias':noticias})

def noticias_mas_comentadas(request):
    noticias=Noticia.objects.all().order_by('-num_comentarios')[:5]
    return render(request,'noticiaspornumcomentario.html', {'noticias':noticias})

def buscar_noticiasporcontenido(request):
    formulario = BusquedaPorContenidoForm()
    noticias = None
    
    if request.method=='POST':
        formulario = BusquedaPorContenidoForm(request.POST)      
        if formulario.is_valid():
            noticias = Noticia.objects.filter(contenido__contains=formulario.cleaned_data['contenido'])
            
    return render(request, 'noticiasporcontenido.html', {'formulario':formulario, 'noticias':noticias})
