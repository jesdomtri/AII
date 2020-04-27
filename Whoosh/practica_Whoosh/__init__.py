# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import os, shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from datetime import datetime
import locale


categorias = []
titulos = []
enlacesNoticias = []
descripciones = []
fechas = []


def extraer_noticias():
    for i in range( 1, 3 ):
        extraer_pagina( "http://www.sensacine.com/noticias/?page=" + str( i ) )


def extraer_pagina( url ):
    resp = requests.get( url )
    soup = BeautifulSoup( resp.content, features = "lxml" )
    datos = soup.find_all( "div", class_ = "news-card" )
    
    for dato in datos:
        meta = dato.find( "div", class_ = "meta" )
        
        categorias.append( meta.find( "div", class_ = "meta-category" ).get_text().split( "-" )[1].strip() )
        
        locale.setlocale(locale.LC_TIME, '')
        
        fechaSeparada = meta.find( "div", class_ = "meta-date" ).get_text().split( "," )[1].split("de")
        fechaUnida = fechaSeparada[0].strip() + "/" + fechaSeparada[1].strip() + "/" + fechaSeparada[2].strip()
        fechaFinal = datetime.strptime( fechaUnida, '%d/%B/%Y' )
        
        fechas.append( fechaFinal)
        
        titulos.append( meta.find( "h2", class_ = "meta-title" ).get_text().strip() )
        
        enlacesNoticias.append( "http://www.sensacine.com/" + meta.find( "a", class_ = "meta-title-link" ).get( 'href' ).strip() )
        
        if meta.find( "div", class_ = "meta-body" ):
            descripciones.append( meta.find( "div", class_ = "meta-body" ).get_text().strip() )
        else:
            descripciones.append( "No hay descripcion" )
        
            
            
def almacenar_datos():
    schem = Schema( categoria = TEXT( stored = True ), titulo = TEXT( stored = True ), enlaceNoticia = TEXT( stored = True ),
                    descripcion = TEXT( stored = True ), fecha = DATETIME( stored = True ) )
    
    if os.path.exists( "Index" ):
        shutil.rmtree( "Index" )
    os.mkdir( "Index" )
    
    ix = create_in( "Index", schema = schem )
    writer = ix.writer()
    i = 0
    extraer_noticias()
    for j in range( len( titulos ) ):
        writer.add_document( categoria = str( categorias[j] ), titulo = str( titulos[j] ), enlaceNoticia = str( enlacesNoticias[j] ),
                             descripcion = str( descripciones[j] ), fecha = fechas[j] )
        i += 1
    writer.commit()
    messagebox.showinfo( "Fin de indexado", "Se han indexado " + str( i ) + " noticias" )
    
    
def buscar_titulo_descripcion():
    def mostrar_lista(event):
        ix=open_dir("Index")
        with ix.searcher() as searcher:
            query = MultifieldParser(["titulo","descripcion"], ix.schema, group=OrGroup).parse(str(en.get()))
            results = searcher.search(query) 
            v = Toplevel()
            v.title("Listado de noticias")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            for r in results: 
                lb.insert(END,r['categoria'])
                lb.insert(END,r['titulo'])
                lb.insert(END,r['fecha'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por titulo o descripcion")
    l = Label(v, text="Introduzca las palabras a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
        


def buscar_descripcion():
    def mostrar_lista(event):
        ix=open_dir("Index")      
        with ix.searcher() as searcher:
            query = QueryParser("descripcion", ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            v = Toplevel()
            v.title("Listado de noticias")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            for r in results:
                lb.insert(END,r['categoria'])
                lb.insert(END,r['titulo'])
                lb.insert(END,r['fecha'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por descripcion")
    l = Label(v, text="Introduzca la frase a buscar en la descripcion:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    
def formatDate( fecha ):
    fechasSplit = fecha.split( ' ' )
    fechaFrom = fechasSplit[0]
    fechaTo = fechasSplit[1]
    dateFrom = datetime.strptime( fechaFrom, '%d/%m/%Y' )
    dateTo = datetime.strptime( fechaTo, '%d/%m/%Y' )
    dates = [dateFrom, dateTo]
    return dates 
    
    
def buscar_fechas():
    def mostrar_lista(event):
        ix=open_dir("Index")      
        with ix.searcher() as searcher:
            fechasQuery = formatDate( str( en.get() ) )
            rango_fecha = '[' + str( fechasQuery[0] ).split( ' ' )[0].strip() + ' TO ' + str( fechasQuery[1] ).split( ' ' )[0].strip() + ']'
            query = QueryParser( "fecha", ix.schema ).parse( rango_fecha )
            results = searcher.search(query)
            v = Toplevel()
            v.title("Listado de noticias")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            for r in results:
                lb.insert(END,r['titulo'])
                lb.insert(END,r['fecha'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Fecha")
    l = Label(v, text="Introduzca rango de fechas DD/MM/AAAA DD/MM/AAAA:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)

    
    
def ventana_principal():
    root = Tk()
    menubar = Menu(root)
    
    datosmenu = Menu( menubar, tearoff = 0 )
    datosmenu.add_command( label = "Cargar", command = almacenar_datos )
    datosmenu.add_separator()   
    datosmenu.add_command( label = "Salir", command = root.quit )
    
    menubar.add_cascade( label = "Datos", menu = datosmenu )
    
    buscarmenu = Menu( menubar, tearoff = 0 )
    buscarmenu.add_command( label = "Título y descripcion", command = buscar_titulo_descripcion )
    buscarmenu.add_command( label = "Descripcion", command = buscar_descripcion )
    buscarmenu.add_command( label = "Rango de fechas", command = buscar_fechas )
    
    menubar.add_cascade( label = "Buscar", menu = buscarmenu )
    
    
    root.config( menu = menubar )
    root.mainloop()        

    
if __name__ == "__main__":
    ventana_principal()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
