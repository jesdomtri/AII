#!/usr/bin/python3
# encoding: utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
import datetime
from tkinter import *
from tkinter import messagebox

url = "https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"
resp = requests.get(url)
soup = BeautifulSoup(resp.content, features = "xml")

items = []
titulos = []
links = []
fechas = []

top = Tk()


def bdCargada():
    for i in soup.findAll('item'):
        items.append(i)
    for i in items:
        titulos.append(i.title.text)
        links.append(i.link.text)
        fechas.append(i.pubDate.text)
    messagebox.showinfo('BD cargada', 'BD cargada correctamente')


text = Text(top)


def mostrarBD():
    window = Toplevel(top)
    text = Text(window)
    for i in range(len(items)):
        text.insert(INSERT, titulos[i] + '\n')
        text.insert(INSERT, links[i] + '\n')
        text.insert(INSERT, fechas[i] + '\n')
        text.insert(INSERT, '\n')
    text.pack()

    
def buscarMes():
    window = Toplevel(top)
    L1 = Label(window, text = "Introduzca el mes (Xxx): ")
    L1.pack(side = LEFT)
    E1 = Entry(window, bd = 5)
    E1.pack(side = RIGHT)
    text = Text(window)

    def confirmarMes():
        text.delete('1.0', END)
        for i in range(len(items)):
            listaFecha = fechas[i].split(' ')
            if E1.get() == listaFecha[2]:
                text.insert(INSERT, titulos[i] + '\n')
                text.insert(INSERT, links[i] + '\n')
                text.insert(INSERT, fechas[i] + '\n')
                text.insert(INSERT, '\n')
            text.pack()

    boton = Button(window, text = 'Confirmar mes', command = confirmarMes)
    boton.pack()


def buscarDia():
    window = Toplevel(top)
    L1 = Label(window, text = "Introduzca el dia (dd/mm/aaaa): ")
    L1.pack(side = LEFT)
    E1 = Entry(window, bd = 5)
    E1.pack(side = RIGHT)
    text = Text(window)

    def confirmarDia():
        text.delete('1.0', END)
        nuevasFechas = []
        for fecha in fechas:
            listaFecha = fecha.split(' ')
            fecha = str(listaFecha[1]) + ' ' + str(listaFecha[2]) + ' ' + str(listaFecha[3]) 
            nuevasFechas.append(datetime.datetime.strptime(fecha, '%d %b %Y').strftime('%d/%m/%Y'))
        for i in range(len(items)):
            if E1.get() == nuevasFechas[i]:
                text.insert(INSERT, titulos[i] + '\n')
                text.insert(INSERT, links[i] + '\n')
                text.insert(INSERT, fechas[i] + '\n')
                text.insert(INSERT, '\n')
            text.pack()

    boton = Button(window, text = 'Confirmar dia', command = confirmarDia)
    boton.pack()

    
B1 = Button(top, text = "Almacenar", command = bdCargada)
B1.pack()
B2 = Button(top, text = "Listar", command = mostrarBD)
B2.pack()
B3 = Button(top, text = 'Buscar por mes', command = buscarMes)
B3.pack()
B4 = Button(top, text = 'Buscar por dia', command = buscarDia)
B4.pack()

mainloop()

