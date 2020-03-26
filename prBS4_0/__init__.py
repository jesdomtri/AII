# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime

titulos = []
enlaces = []
autores = []
fechas = []


def extraerDatos():
    for i in [1, 2, 3]:
        url = "https://www.meneame.net/?page="
        url += str(i)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="lxml")
        for noticia in soup.find_all(class_='center-content'):
            titulos.append(noticia.find_all('a')[0].get_text())
            enlaces.append(noticia.find_all('a')[0].get('href'))
            autores.append(noticia.find_all('a')[2].get_text())
            for f in noticia.find_all('span'):
                if f.get('title') == 'enviado: ':
                    fechas.append(datetime.fromtimestamp(float(f.get('data-ts'))))
    
def imprimirEtiqueta(cursor):
    v = Toplevel()
    v.title("NOTICIAS")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, row[3])
        lb.insert(END, row[4])
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)
   

def almacenarBD():
    conn = sqlite3.connect('noticias.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")
    conn.execute('''CREATE TABLE NOTICIAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       TITULO           TEXT    NOT NULL,
       ENLACE           TEXT    NOT NULL,
       AUTOR        TEXT NOT NULL,
       FECHA           TEXT    NOT NULL);''') 
    extraerDatos()
    for i in range(len(titulos)):
        conn.execute("""INSERT INTO NOTICIAS (TITULO, ENLACE, AUTOR, FECHA) VALUES (?,?,?,?)""",
                     (titulos[i].strip(), enlaces[i], autores[i], fechas[i])) 
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

    
def listarBD():
    conn = sqlite3.connect('noticias.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM NOTICIAS")
    imprimirEtiqueta(cursor)
    conn.close()

    
def buscarAutor():
    conn = sqlite3.connect('noticias.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT AUTOR FROM NOTICIAS")
    
    top = Tk()
    top.title("Buscar por autor")
    
    w = Spinbox(top, values=tuple(set([x[0] for x in cursor])))
    w.pack()
    
    def onClick(event):
        nombreAutor = str(w.get())
        cursor2 = conn.execute('SELECT * FROM NOTICIAS WHERE AUTOR=?', (nombreAutor,))
        
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[3])
            lb.insert(END, row[4])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)

    mainloop()
    
    conn.close()

    
def buscarFecha():
    conn = sqlite3.connect('noticias.db')
    conn.text_factory = str  
    
    top = Tk()
    top.title("Buscar por fecha")
    
    L1 = Label(top, text="Ingresar fecha (aaaa-mm-dd)")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    
    def onClick(event):
        fechaBuscada = str(E1.get()) + ' 00:00:00'
        cursor2 = conn.execute('SELECT * FROM NOTICIAS WHERE FECHA>?', (fechaBuscada,))
        
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[3])
            lb.insert(END, row[4])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)

    mainloop()
    
    conn.close()
    
  
def ventana_principal():
    top = Tk()
    top.title("NOTICIAS")
    
    menubar = Menu(top)

    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Almacenar Noticias", command=almacenarBD)
    datosmenu.add_command(label="Listar Noticias", command=listarBD)
    datosmenu.add_separator()
    datosmenu.add_command(label="Salir", command=top.quit)
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Autor", command=buscarAutor)
    buscarmenu.add_command(label="Fecha", command=buscarFecha)
    buscarmenu.add_separator()
    menubar.add_cascade(label="Buscar", menu=buscarmenu)

    top.config(menu=menubar)
    top.mainloop()
    

if __name__ == "__main__":
    ventana_principal()
    
