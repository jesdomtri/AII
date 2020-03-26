# encoding: utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
import datetime

url = "https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"
resp = requests.get( url )
soup = BeautifulSoup( resp.content, features = "xml" )
# #print soup.prettify()

items = soup.findAll( 'item' )
titulos = [i.title.text for i in items]
links = [i.link.text for i in items]
fechasNoLimpias = [i.pubDate.text for i in items]
fechas = []
for fecha in fechasNoLimpias:
    listaFecha = fecha.split( ' ' )
    fecha = str( listaFecha[1] ) + ' ' + str( listaFecha[2] ) + ' ' + str( listaFecha[3] )
    fechas.append( datetime.datetime.strptime( fecha, '%d %b %Y' ).strftime( '%d/%m/%Y' ) )

for i in range( len( items ) ):
    print( 'Titulo: ' + titulos[i] )
    print( 'Link: ' + links[i] )
    print( 'Fecha: ' + fechas[i] )
    print( '\n' )

mes = input( 'Introduzca un mes: ' )
dia = input( 'Introduzca un dia: ' )

print('Noticias con fecha: ' + dia + '/' + mes)

for i in range( len( items ) ):
    listaFecha = fechas[i].split( '/' )
    if dia == listaFecha[0] and mes == listaFecha[1]:
        print( 'Titulo: ' + titulos[i] )
        print( 'Fecha: ' + fechas[i] )
        print( '\n' )