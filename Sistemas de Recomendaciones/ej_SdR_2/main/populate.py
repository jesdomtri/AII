from main.models import Book, Rating
from datetime import datetime

path = "datos"

def deleteTables():  
    Rating.objects.all().delete()
    Book.objects.all().delete()
    

def populateLibros():
    print("Cargando libros...")
        
    lista=[]
    fileobj=open(path+"\\books.csv", "r")
    for line in fileobj.readlines()[1:]:
        rip = line.split(';')
        l=Book(isbn=int(rip[0]), titulo=rip[1], autor=rip[2], anyo=rip[3], editor=rip[4])
        lista.append(l)
    Book.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Libros añadidos: " + str(Book.objects.count()))
    print("---------------------------------------------------------")


def populateRating():
    print("Loading ratings...")
        
    lista=[]
    fileobj=open(path+"\\ratings.csv", "r")
    for line in fileobj.readlines()[1:]:
        rip = line.split(';')
        l=Rating(user=int(rip[0]), isbn=int(rip[1]), rating=int(rip[2]))
        lista.append(l)
    Rating.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Libros añadidos: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    deleteTables()
    populateLibros()
    populateRating()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()