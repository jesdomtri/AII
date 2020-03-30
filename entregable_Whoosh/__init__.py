# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import os, shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser, MultifieldParser

url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
resp = requests.get( url )
soup = BeautifulSoup( resp.content, features = "lxml" )

equiposLocales = []
equiposVisitantes = []
goles = []
fechas = []
autores = []
titulos = []
resumenes = []

links = []

def extraerDatos():
    
    encontrarEquipos = soup.find_all( class_ = "nombre-equipo" )[:60]
    for i in range( len( encontrarEquipos ) ):
        if i % 2 == 0:
            equiposLocales.append( encontrarEquipos[i].text )
        else:
            equiposVisitantes.append( encontrarEquipos[i].text )
            
    resultados = soup.find_all( class_ = "resultado" )[:30]
    for resultado in resultados:
        goles.append( resultado.get_text().strip() )
        links.append( 'https://resultados.as.com' + resultado.get( 'href' ) )
    
    for link in links:
        respLink = requests.get( link )
        soupLink = BeautifulSoup( respLink.content, features = "lxml" )
        
        cronicas = soupLink.find( "div", class_ = "cont-cuerpo-noticia" )

        if cronicas:    
            titulos.append( cronicas.find( "h2", class_ = "live-title" ).get_text().strip() )
            autores.append( cronicas.find( "p", class_ = "ntc-autor" ).get_text().strip() )
            fechas.append( cronicas.find( "time", class_ = 'ntc-time' ).find( 'span' ).get_text().strip() )
            resumenes.append( cronicas.find( 'div', class_ = "cf" ).get_text().strip() )
        else:
            titulos.append( 'No hay titulo' )
            autores.append( 'No hay autor' )
            fechas.append( 'No hay fecha' )
            resumenes.append( 'No hay resumen' )

        
def almacenar_datos():
    
    schem = Schema( jornada = TEXT( stored = True ), equipoLocal = TEXT( stored = True ), equipoVisitante = TEXT( stored = True ), resultado = TEXT( stored = True ),
                   titulo = TEXT( stored = True ), autor = TEXT( stored = True ), fecha = TEXT( stored = True ), resumen = TEXT( stored = True ) )
    
    if os.path.exists( "Index" ):
        shutil.rmtree( "Index" )
    os.mkdir( "Index" )
    
    ix = create_in( "Index", schema = schem )
    writer = ix.writer()
    i = 0
    extraerDatos()
    contador = 0
    for j in range( len( goles ) ):
        if j % 10 == 0:
            contador += 1
        writer.add_document( jornada = str( contador ), equipoLocal = str( equiposLocales[j] ), equipoVisitante = str( equiposVisitantes[j] ), resultado = str( goles[j] ),
                            titulo = titulos[j], autor = str( autores[j] ), fecha = str( fechas[j] ), resumen = str( resumenes[j] ) )    
        i += 1
    writer.commit()
    messagebox.showinfo( "Fin de indexado", "Se han indexado " + str( i ) + " partidos" )

        
def buscar_noticia():

    def mostrar_lista( event ):
        lb.delete( 0, END ) 
        ix = open_dir( "Index" )      
        with ix.searcher() as searcher:
            query = QueryParser( "resumen", ix.schema ).parse( str( en.get() ) )
            results = searcher.search( query )
            for r in results:
                lb.insert( END, r['fecha'] )
                lb.insert( END, r['titulo'] )
                lb.insert( END, r['autor'] )
                lb.insert( END, '' )

    v = Toplevel()
    v.title( "Busqueda por palabra" )
    f = Frame( v )
    f.pack( side = TOP )
    l = Label( f, text = "Introduzca la palabra del resumen:" )
    l.pack( side = LEFT )
    en = Entry( f )
    en.bind( "<Return>", mostrar_lista )
    en.pack( side = LEFT )
    sc = Scrollbar( v )
    sc.pack( side = RIGHT, fill = Y )
    lb = Listbox( v, yscrollcommand = sc.set )
    lb.pack( side = BOTTOM, fill = BOTH )
    sc.config( command = lb.yview )
        
        
def buscar_equipo():

    def mostrar_lista(event):
        lb.delete(0, END) 
        ix = open_dir("Index")      
        with ix.searcher() as searcher:
            query =  MultifieldParser( ["equipoLocal", "equipoVisitante"], ix.schema ).parse( str(en.get()) )
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['jornada'])
                lb.insert(END, r['equipoLocal'])
                lb.insert(END, r['equipoVisitante'])
                lb.insert(END, r['resultado'])
                lb.insert(END, '')

    v = Toplevel()
    v.title("Busqueda por equipo")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el nombre del equipo:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)
            
        
def ventana_principal():
        
    root = Tk()
    menubar = Menu( root )
    
    datosmenu = Menu( menubar, tearoff = 0 )
    datosmenu.add_command( label = "Cargar", command = almacenar_datos )
    datosmenu.add_separator()   
    datosmenu.add_command( label = "Salir", command = root.quit )
    
    menubar.add_cascade( label = "Datos", menu = datosmenu )
    
    buscarmenu = Menu( menubar, tearoff = 0 )
    buscarmenu.add_command(label="Noticia", command=buscar_noticia)
    buscarmenu.add_command(label="Equipo", command=buscar_equipo)
    
    menubar.add_cascade( label = "Buscar", menu = buscarmenu )
        
    root.config( menu = menubar )
    root.mainloop()        


if __name__ == "__main__":
    ventana_principal()
