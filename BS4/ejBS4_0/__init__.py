#!/usr/bin/python3
# encoding: utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import sqlite3
from builtins import str

url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
resp = requests.get(url)
soup = BeautifulSoup(resp.content, features = "lxml")

equiposLocales = []
equiposVisitantes = []
golesLocales = []
golesVisitantes = []
links = []

top = Tk()


def extraerDatos():
    listaPartidos = []
    
    encontrarEquipos = soup.find_all(class_ = "nombre-equipo")
    for i in range(len(encontrarEquipos)):
        if i % 2 == 0:
            equiposLocales.append(encontrarEquipos[i].text)
        else:
            equiposVisitantes.append(encontrarEquipos[i].text)
            
    resultados = soup.find_all(class_ = "resultado")
    for resultado in resultados:
        golesLocales.append(resultado.text.split('-')[0].strip())
        golesVisitantes.append(resultado.text.split('-')[1].strip())
        links.append('https://resultados.as.com' + resultado.get('href'))
    
    for i in range(len(golesLocales)):
        partido = [equiposLocales[i], equiposVisitantes[i], golesLocales[i], golesVisitantes[i], links[i]]
        listaPartidos.append(partido)
            
    return listaPartidos

def almacenarBD():
    conn = sqlite3.connect('partidos.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS PARTIDOS")   
    conn.execute('''CREATE TABLE PARTIDOS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       JORNADA           INTEGER    NOT NULL,
       EQUIPO_LOCAL           TEXT    NOT NULL,
       EQUIPO_VISITANTE        TEXT NOT NULL,
       GOLES_LOCAL           INTEGER    NOT NULL,
       GOLES_VISITANTE           INTEGER    NOT NULL,
       LINK           TEXT    NOT NULL);''')
    partidos = extraerDatos()
    contador = 0
    for i in range(len(partidos)):
        if i % 10 == 0:
            contador += 1
        conn.execute("""INSERT INTO PARTIDOS (JORNADA, EQUIPO_LOCAL, EQUIPO_VISITANTE, GOLES_LOCAL, GOLES_VISITANTE, LINK) VALUES (?,?,?,?,?,?)""", (contador,
            partidos[i][0], partidos[i][1], partidos[i][2], partidos[i][3], partidos[i][4]))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PARTIDOS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

    
def listarBD():
    conn = sqlite3.connect('partidos.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM PARTIDOS")
    imprimirEtiqueta(cursor)
    conn.close()


def imprimirEtiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill = Y)
    lb = Listbox(v, width = 150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, 'Jornada: ', row[1])
        lb.insert(END, 'Equipo local: ' + str(row[2]))
        lb.insert(END, 'Equipo visitante: ' + str(row[3]))
        lb.insert(END, 'Goles local: ' + str(row[4]))
        lb.insert(END, 'Goles visitante: ' + str(row[5]))
        lb.insert(END, 'Link: ' + str(row[6]))
        lb.insert(END, '')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

    
B1 = Button(top, text = "Almacenar", command = almacenarBD)
B1.pack()
B2 = Button(top, text = "Listar", command = listarBD)
B2.pack()

mainloop()

