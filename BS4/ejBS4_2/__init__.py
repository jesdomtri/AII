# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import sqlite3
from builtins import str

enlaces = []
titulos = []
titulosOriginales = []
paises = []
fechaEstrenoSpain = []
directores = []
generos = []


def extraerEnlaces():
    for i in [1, 2]:
        url = "https://www.elseptimoarte.net/estrenos/"
        url += str(i)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="lxml")
        peliculas = soup.find(class_='elements').find_all('li')
        for p in peliculas:
            enlaces.append('https://www.elseptimoarte.net/peliculas' + p.find('h3').find('a').get('href'))


def extraerDatos():
    extraerEnlaces()
    for enlace in enlaces:
        resp = requests.get(enlace)
        soup = BeautifulSoup(resp.content, features="lxml")
        datos = soup.find('section', class_='highlight').find('div').find('dl').find_all('dt')

        for dato in datos:
            if dato.text == 'Título':
                titulos.append(dato.find_next_sibling("dd").text.lstrip())
            
            elif dato.text == 'Título original':
                titulosOriginales.append(dato.find_next_sibling("dd").text.lstrip())
            
            elif dato.text == 'Estreno en España':
                fechaEstrenoSpain.append(dato.find_next_sibling("dd").text.lstrip())
            
            elif dato.text == 'País':
                paisesLimpios = [p for p in dato.find_next_sibling('dd').stripped_strings]
                pais = ''
                for p in paisesLimpios:
                    pais += p.replace('  ','')
                paises.append(pais)
            
            elif dato.text == 'Director':
                directores.append(dato.find_next_sibling("dd").text.lstrip())

        
        generos.append(soup.find(class_='categorias').text.replace('\n','').replace(' ','').lstrip())


def almacenarBD():
    conn = sqlite3.connect('peliculas.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS PELICULAS")
    conn.execute('''CREATE TABLE PELICULAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       TITULO           TEXT    NOT NULL,
       ORIGINAL           TEXT    NOT NULL,
       FECHA        TEXT NOT NULL,
       PAIS           TEXT    NOT NULL,
       DIRECTOR           TEXT    NOT NULL,
       GENERO           TEXT    NOT NULL);''') 
    extraerDatos()
    for i in range(len(titulos)):
        conn.execute("""INSERT INTO PELICULAS (TITULO, ORIGINAL, FECHA, PAIS, DIRECTOR, GENERO) VALUES (?,?,?,?,?,?)""",
                     (titulos[i], titulosOriginales[i], fechaEstrenoSpain[i], paises[i], directores[i], generos[i])) 
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PELICULAS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def buscarTitulo():
    conn = sqlite3.connect('peliculas.db')
    conn.text_factory = str  
    top = Tk()
    top.title("Buscar por titulo")
    L1 = Label(top, text="Ingresar palabra en el titulo: ")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    
    def onClick(event):
        titulo = str(E1.get())
        cursor2 = conn.execute('SELECT * FROM PELICULAS WHERE TITULO LIKE ?', ('%' + titulo+ '%',))
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[4])
            lb.insert(END, row[5])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)
    mainloop()
    conn.close()

def buscarFecha():
    conn = sqlite3.connect('peliculas.db')
    conn.text_factory = str  
    top = Tk()
    top.title("Buscar por fecha")
    L1 = Label(top, text="Ingresar fecha: ")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    
    def onClick(event):
        fecha = str(E1.get())
        cursor2 = conn.execute('SELECT * FROM PELICULAS WHERE FECHA=?', (fecha,))
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[3])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)
    mainloop()
    conn.close()
    
def buscarGenero():
    conn = sqlite3.connect('peliculas.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT GENERO FROM PELICULAS")
    top = Tk()
    top.title("Buscar por genero")
    generos1 = []
    for u in set([x[0] for x in cursor]):
        if u.find(','):
            u3 = u.split(',')
            for u2 in u3:
                generos1.append(u2.strip())
        else:
            generos1.append(u.strip())
    w = Spinbox(top, values=tuple(set(generos1)))
    w.pack()

    def onClick(event):
        entry = str(w.get())
        cursor2 = conn.execute('SELECT * FROM PELICULAS WHERE GENERO LIKE ?', ('%' + entry + '%',))
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[3])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)

    top.bind('<Return>', onClick)
    mainloop()
    conn.close()

    
def ventana_principal():
    top = Tk()
    top.title("PELICULAS")
    
    menubar = Menu(top)

    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Almacenar Peliculas", command=almacenarBD)
    datosmenu.add_separator()
    datosmenu.add_command(label="Salir", command=top.quit)
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Titulo", command=buscarTitulo)
    buscarmenu.add_command(label="Fecha", command=buscarFecha)
    buscarmenu.add_separator()
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
    
    porgenero = Menu(menubar, tearoff=0)
    porgenero.add_command(label="Buscar por genero", command=buscarGenero)
    porgenero.add_separator()
    menubar.add_cascade(label="Buscar por genero", menu=porgenero)

    top.config(menu=menubar)
    top.mainloop()
  
    
if __name__ == "__main__":
    ventana_principal()