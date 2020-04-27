# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import sqlite3
from builtins import str

url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
resp = requests.get(url)
soup = BeautifulSoup(resp.content, features="lxml")

equiposLocales = []
equiposVisitantes = []
golesLocales = []
golesVisitantes = []
links = []

top = Tk()


def extraerDatos():
    listaPartidos = []
    
    encontrarEquipos = soup.find_all(class_="nombre-equipo")
    for i in range(len(encontrarEquipos)):
        if i % 2 == 0:
            equiposLocales.append(encontrarEquipos[i].text)
        else:
            equiposVisitantes.append(encontrarEquipos[i].text)
            
    resultados = soup.find_all(class_="resultado")
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
        conn.execute("""INSERT INTO PARTIDOS (JORNADA, EQUIPO_LOCAL, EQUIPO_VISITANTE, 
            GOLES_LOCAL, GOLES_VISITANTE, LINK) VALUES (?,?,?,?,?,?)""", (contador,
            partidos[i][0], partidos[i][1], partidos[i][2], partidos[i][3], partidos[i][4]))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PARTIDOS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


def imprimirEtiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END, 'Jornada: ', row[1])
        lb.insert(END, 'Equipo local: ' + str(row[2]))
        lb.insert(END, 'Equipo visitante: ' + str(row[3]))
        lb.insert(END, 'Goles local: ' + str(row[4]))
        lb.insert(END, 'Goles visitante: ' + str(row[5]))
        lb.insert(END, 'Link: ' + str(row[6]))
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)    


def listarBD():
    conn = sqlite3.connect('partidos.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM PARTIDOS")
    imprimirEtiqueta(cursor)
    conn.close()

    
def buscarJornada():
    conn = sqlite3.connect('partidos.db')
    conn.text_factory = str  
    
    top = Tk()
    top.title("Buscar por jornada")
    
    L1 = Label(top, text="Ingresar jornada: ")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    
    def onClick(event):
        jornada = str(E1.get())
        cursor = conn.execute('SELECT * FROM PARTIDOS WHERE JORNADA=?', (jornada,))
        
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor:
            lb.insert(END, 'Jornada: ', row[1])
            lb.insert(END, 'Equipo local: ' + str(row[2]))
            lb.insert(END, 'Equipo visitante: ' + str(row[3]))
            lb.insert(END, 'Goles local: ' + str(row[4]))
            lb.insert(END, 'Goles visitante: ' + str(row[5]))
            lb.insert(END, 'Link: ' + str(row[6]))
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)
    
    mainloop()
    
    conn.close()

    
def buscarGoles():
    conn = sqlite3.connect('partidos.db')
    conn.text_factory = str  
    
    top = Tk()
    top.title("Buscar goles")
    
    L1 = Label(top, text="Ingresar jornada: ")
    L1.place(x = 10,y = 10)
    E1 = Entry(top, bd=5)
    E1.place(x = 150,y = 10)
    
    L2 = Label(top, text="Ingresar equipo local: ")
    L2.place(x = 10,y = 50)
    E2 = Entry(top, bd=5)
    E2.place(x = 150,y = 50)
    
    L3 = Label(top, text="Ingresar equipo visitante: ")
    L3.place(x = 10,y = 150)
    E3 = Entry(top, bd=5)
    E3.place(x = 150,y = 150)
    
    def buscar():
        jornada = str(E1.get())
        equipoLocal = str(E2.get())
        equipoVisitante = str(E3.get())
        
        cursor = conn.execute('SELECT LINK FROM PARTIDOS WHERE JORNADA=? AND EQUIPO_LOCAL=? AND EQUIPO_VISITANTE=?', (jornada, equipoLocal, equipoVisitante))
        
        url2 = cursor.fetchone()[0]
        resp2 = requests.get(url2)
        soup2 = BeautifulSoup(resp2.content, features="lxml")
        
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    B1 = Button(top, text="Buscar", command=buscar)
    B1.place(x = 100, y = 100)
    
    top.geometry("300x300+10+10")
    
    mainloop()
    
    conn.close()

    
B1 = Button(top, text="Almacenar", command=almacenarBD)
B1.pack()
B2 = Button(top, text="Listar", command=listarBD)
B2.pack()
B3 = Button(top, text="Buscar por jornada", command=buscarJornada)
B3.pack()
B3 = Button(top, text="Buscar por goles", command=buscarGoles)
B3.pack()

mainloop()
