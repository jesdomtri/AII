#encoding:utf-8
from main.models import Bodega, Vino, Denominacion, Uva
from main.forms import BusquedaPorUvaForm
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib.request
import lxml
from django.db.models import Avg

def cargaBD():
    num_vinos = 0

    Bodega.objects.all().delete()
    Vino.objects.all().delete()
    Denominacion.objects.all().delete()
    Uva.objects.all().delete()

    url = urllib.request.urlopen("https://www.vinissimus.com/es/vinos/tinto/")
    bs = BeautifulSoup(url, "lxml")
    lista_vinos = bs.find_all('div', class_='product-list-item')
    for informacion in lista_vinos:
        nombre = informacion.find('h2', class_='title').text.strip()
        
        precio = float(informacion.find('p', class_='price').get_text().strip().split(' ')[0].replace(',','.'))
        
        denominacion = informacion.find(class_='region').get_text().strip()
        
        urlVino = 'https://www.vinissimus.com' + informacion.find('div', class_='details').find('a').get('href')
        soup = BeautifulSoup(urllib.request.urlopen(urlVino), "lxml")
        bodega = soup.find(class_='cellar').get_text().strip()

        uvas = "".join(soup.find('div', class_='tags').stripped_strings)
        uvas = uvas.split(sep="/")

        puntuacion = informacion.find("span", class_='opinion-badge')
        if puntuacion:
            puntuacion = puntuacion.get_text().replace('★', '')
        else:
            puntuacion = None

        bodega_obj, creado = Bodega.objects.get_or_create(nombre=bodega)
        denominacion_obj, creado = Denominacion.objects.get_or_create(nombre=denominacion)

        lista_uvas_obj = []
        for uva in uvas:
            uva_obj, creado = Uva.objects.get_or_create(nombre=uva)
            lista_uvas_obj.append(uva_obj)

        v = Vino.objects.create(nombre = nombre, precio = precio, 
                            denominacion = denominacion_obj, bodega = bodega_obj,
                            puntuacion = puntuacion)
        
        for u in lista_uvas_obj:
            v.uva.add(u)
        
        num_vinos = num_vinos + 1
    
    return(num_vinos)

def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_vinos = cargaBD()
            mensaje="Se han almacenado: " + str(num_vinos) + " vinos"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def inicio(request):
    num_vinos=Vino.objects.all().count()
    return render(request,'inicio.html', {'num_vinos':num_vinos})

def lista_vinos(request):
    vinos=Vino.objects.all()
    return render(request,'vinos.html', {'vinos':vinos})

def mejores_vinos(request):
    vinos=Vino.objects.all().order_by('-puntuacion')[:3]
    return render(request,'mejoresvinos.html', {'vinos':vinos})

def buscar_por_uvas(request):
    formulario = BusquedaPorUvaForm()
    vinos = None
    if request.method=='POST':
        formulario = BusquedaPorUvaForm(request.POST)
        if formulario.is_valid():
            uva = Uva.objects.get(id=formulario.cleaned_data['uva'].id)
            vinos = uva.vino_set.all()
    return render(request, 'busquedaporuva.html', {'formulario':formulario, 'vinos':vinos})

def lista_vinos_por_denominacion(request):
    vinos=Vino.objects.all().order_by('denominacion')
    denom = Denominacion.objects.values('nombre').annotate(average_precio=Avg('vino__precio'))
    return render(request,'vinospordenominacion.html', {'vinos':vinos, 'denom':denom})

def mejor_bodega(request):
    bodegas = Bodega.objects.exclude(vino__puntuacion=None).values('nombre').annotate(relacion=Avg('vino__precio')/Avg('vino__puntuacion')).order_by('-relacion')[:1]
    return render(request,'mejorbodega.html', {'bodegas':bodegas})