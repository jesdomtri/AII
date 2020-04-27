# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import os, shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser
from datetime import datetime

enlaces = []
titulos = []
titulosOriginales = []
paises = []
fechaEstrenoSpain = []
directores = []
generos = []
sinopsis = []


def extraerEnlaces():
    url = "https://www.elseptimoarte.net/estrenos/"
    resp = requests.get( url )
    soup = BeautifulSoup( resp.content, features = "lxml" )
    peliculas = soup.find( class_ = 'elements' ).find_all( 'li' )
    for p in peliculas:
        enlaces.append( 'https://www.elseptimoarte.net/peliculas' + p.find( 'h3' ).find( 'a' ).get( 'href' ) )


def extraerDatos():
    extraerEnlaces()
    contador = 1
    for enlace in enlaces:
        resp = requests.get( enlace )
        soup = BeautifulSoup( resp.content, features = "lxml" )
        datos = soup.find( 'section', class_ = 'highlight' ).find( 'div' ).find( 'dl' ).find_all( 'dt' )

        for dato in datos:
            if dato.text == 'Título':
                titulos.append( dato.find_next_sibling( "dd" ).text.lstrip() )
            
            elif dato.text == 'Título original':
                titulosOriginales.append( dato.find_next_sibling( "dd" ).text.lstrip() )
            
            elif dato.text == 'Estreno en España':
                f = dato.find_next_sibling( "dd" ).text.lstrip()
                f = datetime.strptime( f, '%d/%m/%Y' )
                fechaEstrenoSpain.append( f )
            
            elif dato.text == 'País':
                paisesLimpios = [p for p in dato.find_next_sibling( 'dd' ).stripped_strings]
                pais = ''
                for p in paisesLimpios:
                    pais += p.replace( '  ', '' )
                paises.append( pais )
            
            elif dato.text == 'Director':
                directores.append( dato.find_next_sibling( "dd" ).text.lstrip() )
            
        generos.append( soup.find( class_ = 'categorias' ).text.replace( '\n', '' ).replace( ' ', '' ).lstrip() )
    
        sinopsis.append( soup.find_all( 'section', class_ = 'highlight' )[1].find( 'div' ).get_text().strip() )
        
        if len( titulos ) != contador:
            titulos.append( 'No hay título' )
        if len( titulosOriginales ) != contador:
            titulosOriginales.append( 'No hay título original' )
        if len( fechaEstrenoSpain ) != contador:
            fechaEstrenoSpain.append( 'No hay fecha de estreno en España' )
        if len( paises ) != contador:
            paises.append( 'No hay países' )
        if len( directores ) != contador:
            directores.append( 'No hay director' )
        if len( generos ) != contador:
            generos.append( 'No hay géneros' )
        if len( sinopsis ) != contador:
            sinopsis.append( 'No hay sinopsis' )
        
        contador += 1
        
        
def almacenar_datos():
    
    schem = Schema( titulo = TEXT( stored = True ), tituloOriginal = TEXT( stored = True ), fechaEstrenoSpain = DATETIME( stored = True ), paises = TEXT( stored = True ),
                   generos = TEXT( stored = True ), director = TEXT( stored = True ), sinopsis = TEXT( stored = True ) )
    
    if os.path.exists( "Index" ):
        shutil.rmtree( "Index" )
    os.mkdir( "Index" )
    
    ix = create_in( "Index", schema = schem )
    writer = ix.writer()
    i = 0
    extraerDatos()
    for j in range( len( titulos ) ):
        writer.add_document( titulo = str( titulos[j] ), tituloOriginal = str( titulosOriginales[j] ), fechaEstrenoSpain = fechaEstrenoSpain[j] , paises = str( paises[j] ),
                            generos = generos[j], director = str( directores[j] ), sinopsis = str( sinopsis[j] ) )    
        i += 1
    writer.commit()
    messagebox.showinfo( "Fin de indexado", "Se han indexado " + str( i ) + " películas" )


def buscar_titulo_sinopsis():

    def mostrar_lista( event ):
        lb.delete( 0, END ) 
        ix = open_dir( "Index" )      
        with ix.searcher() as searcher:
            query = MultifieldParser( ["titulo", "sinopsis"], ix.schema ).parse( str( en.get() ) )
            results = searcher.search( query )
            for r in results:
                lb.insert( END, r['titulo'] )
                lb.insert( END, r['tituloOriginal'] )
                lb.insert( END, r['paises'] )
                lb.insert( END, '' )

    v = Toplevel()
    v.title( "Busqueda por palabra" )
    f = Frame( v )
    f.pack( side = TOP )
    l = Label( f, text = "Introduzca la palabra del título o sinopsis:" )
    l.pack( side = LEFT )
    en = Entry( f )
    en.bind( "<Return>", mostrar_lista )
    en.pack( side = LEFT )
    sc = Scrollbar( v )
    sc.pack( side = RIGHT, fill = Y )
    lb = Listbox( v, yscrollcommand = sc.set )
    lb.pack( side = BOTTOM, fill = BOTH )
    sc.config( command = lb.yview )
        
        
def buscar_generos():

    def mostrar_lista( event ):
        lb.delete( 0, END ) 
        ix = open_dir( "Index" )      
        with ix.searcher() as searcher:
            query = QueryParser( "generos", ix.schema ).parse( str( en.get() ) )
            results = searcher.search( query )
            for r in results:
                lb.insert( END, r['titulo'] )
                lb.insert( END, r['tituloOriginal'] )
                lb.insert( END, r['paises'] )
                lb.insert( END, '' )

    v = Toplevel()
    v.title( "Busqueda por géneros" )
    f = Frame( v )
    f.pack( side = TOP )
    l = Label( f, text = "Introduzca el género:" )
    l.pack( side = LEFT )
    en = Entry( f )
    en.bind( "<Return>", mostrar_lista )
    en.pack( side = LEFT )
    sc = Scrollbar( v )
    sc.pack( side = RIGHT, fill = Y )
    lb = Listbox( v, yscrollcommand = sc.set )
    lb.pack( side = BOTTOM, fill = BOTH )
    sc.config( command = lb.yview )
    
    
def formatDate( fecha ):
    fechasSplit = fecha.split( ' ' )
    fechaFrom = fechasSplit[0]
    fechaTo = fechasSplit[1]
    dateFrom = datetime.strptime( fechaFrom, '%Y%m%d' )
    dateTo = datetime.strptime( fechaTo, '%Y%m%d' )
    dates = [dateFrom, dateTo]
    return dates

    
def buscar_fechas():

    def mostrar_lista( event ):
        lb.delete( 0, END ) 
        ix = open_dir( "Index" )      
        with ix.searcher() as searcher:
            fechasQuery = formatDate( str( en.get() ) )
            rango_fecha = '[' + str( fechasQuery[0] ).split( ' ' )[0].strip() + ' TO ' + str( fechasQuery[1] ).split( ' ' )[0].strip() + ']'
            query = QueryParser( "fechaEstrenoSpain", ix.schema ).parse( rango_fecha )
            results = searcher.search( query )
            for r in results:
                lb.insert( END, r['titulo'] )
                lb.insert( END, r['fechaEstrenoSpain'] )
                lb.insert( END, '' )

    v = Toplevel()
    v.title( "Busqueda por rango de fechas" )
    f = Frame( v )
    f.pack( side = TOP )
    l = Label( f, text = "Introduzca dos fechas ( AAAAMMDD AAAAMMDD ):" )
    l.pack( side = LEFT )
    en = Entry( f )
    en.bind( "<Return>", mostrar_lista )
    en.pack( side = LEFT )
    sc = Scrollbar( v )
    sc.pack( side = RIGHT, fill = Y )
    lb = Listbox( v, yscrollcommand = sc.set )
    lb.pack( side = BOTTOM, fill = BOTH )
    sc.config( command = lb.yview )
    
        
def ventana_principal():
        
    root = Tk()
    menubar = Menu( root )
    
    datosmenu = Menu( menubar, tearoff = 0 )
    datosmenu.add_command( label = "Cargar", command = almacenar_datos )
    datosmenu.add_separator()   
    datosmenu.add_command( label = "Salir", command = root.quit )
    
    menubar.add_cascade( label = "Datos", menu = datosmenu )
    
    buscarmenu = Menu( menubar, tearoff = 0 )
    buscarmenu.add_command( label = "Título y sinopsis", command = buscar_titulo_sinopsis )
    buscarmenu.add_command( label = "Género", command = buscar_generos )
    buscarmenu.add_command( label = "Rango de fechas", command = buscar_fechas )
    
    menubar.add_cascade( label = "Buscar", menu = buscarmenu )
        
    root.config( menu = menubar )
    root.mainloop()        
    
    
if __name__ == '__main__':
    ventana_principal()
