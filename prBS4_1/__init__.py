# encoding:utf-8
from bs4 import BeautifulSoup
from pip._vendor import requests
from tkinter import *
from tkinter import messagebox
import sqlite3
from builtins import str

nombres = []
precios = []
origenes = []
bodegas = []
tipoUvas = []


def extraerDatos():
    for i in [0, 50]:
        url = "https://www.vinissimus.com/es/vinos/tinto/index.html?start="
        url += str(i)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="lxml")
        tabla = soup.table
        for informacion in tabla.find_all(class_='info'):
            nombres.append(informacion.find('h3').find('a').text.strip())
            precio = [p for p in informacion.find(class_='price').stripped_strings]
            if len(precio) == 2:
                precios.append(precio[1])
            else:
                precios.append(precio[0])
            origenes.append(informacion.find(class_='type').text.replace('\n', '').replace('\t', '').split(',')[1].split('(')[0].strip())
            bodegas.append(informacion.find(class_='owner').text.strip())
            uvas = informacion.find(class_='grape').text.replace('\n', '').replace('\t', '').strip().split(',')
            uvaF = uvas[0]
            uvas.pop(0)
            for uva in uvas:
                uvaF += ', ' + uva.strip()
            tipoUvas.append(uvaF)

            
def almacenarBD():
    conn = sqlite3.connect('vinos.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS VINOS")
    conn.execute('''CREATE TABLE VINOS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       NOMBRE           TEXT    NOT NULL,
       PRECIO           TEXT    NOT NULL,
       ORIGEN        TEXT NOT NULL,
       BODEGA           TEXT    NOT NULL,
       UVAS           TEXT    NOT NULL);''') 
    extraerDatos()
    for i in range(len(nombres)):
        conn.execute("""INSERT INTO VINOS (NOMBRE, PRECIO, ORIGEN, BODEGA, UVAS) VALUES (?,?,?,?,?)""",
                     (nombres[i], precios[i], origenes[i], bodegas[i], tipoUvas[i])) 
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM VINOS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    

def buscarDenominacion():
    conn = sqlite3.connect('vinos.db')
    conn.text_factory = str  
    top = Tk()
    top.title("Buscar por denominacion")
    L1 = Label(top, text="Ingresar origen: ")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    
    def onClick(event):
        origen = str(E1.get())
        cursor2 = conn.execute('SELECT * FROM VINOS WHERE ORIGEN=?', (origen,))
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[2])
            lb.insert(END, row[4])
            lb.insert(END, row[3])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)
    mainloop()
    conn.close()

    
def buscarBodega():
    conn = sqlite3.connect('vinos.db')
    conn.text_factory = str  
    top = Tk()
    top.title("Buscar por bodega")
    L1 = Label(top, text="Ingresar bodega: ")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    
    def onClick(event):
        bodega = str(E1.get())
        cursor2 = conn.execute('SELECT * FROM VINOS WHERE BODEGA=?', (bodega,))
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[2])
            lb.insert(END, row[4])
            lb.insert(END, row[3])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)
    
    top.bind('<Return>', onClick)
    mainloop()
    conn.close()


def buscarUva():
    conn = sqlite3.connect('vinos.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT UVAS FROM VINOS")
    top = Tk()
    top.title("Buscar por uva")
    uvas1 = []
    for u in set([x[0] for x in cursor]):
        if u.find(','):
            u3 = u.split(',')
            for u2 in u3:
                uvas1.append(u2.strip())
        else:
            uvas1.append(u.strip())
    w = Spinbox(top, values=tuple(set(uvas1)))
    w.pack()

    def onClick(event):
        uva = str(w.get())
        cursor2 = conn.execute('SELECT * FROM VINOS WHERE UVAS LIKE ?', ('%' + uva + '%',))
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, height=150, yscrollcommand=sc.set)
        for row in cursor2:
            lb.insert(END, row[1])
            lb.insert(END, row[5])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)

    top.bind('<Return>', onClick)
    mainloop()
    conn.close()


def ventana_principal():
    top = Tk()
    top.title("VINITOS")
    
    menubar = Menu(top)

    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Almacenar Vinos", command=almacenarBD)
    datosmenu.add_separator()
    datosmenu.add_command(label="Salir", command=top.quit)
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Denominacion", command=buscarDenominacion)
    buscarmenu.add_command(label="Bodega", command=buscarBodega)
    buscarmenu.add_command(label="Uvas", command=buscarUva)
    buscarmenu.add_separator()
    menubar.add_cascade(label="Buscar", menu=buscarmenu)

    top.config(menu=menubar)
    top.mainloop()
  
    
if __name__ == "__main__":
    ventana_principal()
