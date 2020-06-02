from main.models import Anime, Rating
from datetime import datetime

path = "datos"

def deleteTables():
    Anime.objects.all().delete()  
    Rating.objects.all().delete()
    


def populateAnimes():
    print("Cargando animes...")
        
    lista=[]
    dict_categorias = {}
    fileobj=open(path+"\\anime.csv", "r")
    for line in fileobj.readlines()[1:]:
        rip = line.split(';')
        l=Anime(animeid=int(rip[0]), titulo=rip[1], generos=rip[2], formato=rip[3], numepisodios=rip[4])
        lista.append(l)


    Anime.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso

    print("Animes añadidos: " + str(Anime.objects.count()))
    print("---------------------------------------------------------")


def populateRating():
    print("Cargando ratings...")
        
    lista=[]
    fileobj=open(path+"\\ratings.csv", "r")
    for line in fileobj.readlines()[1:]:
        rip = line.split(';')
        l=Rating(user=int(rip[0]), animeid=int(rip[1]), rating=int(rip[2]))
        lista.append(l)
    Rating.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Ratings añadidos: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    deleteTables()
    populateAnimes()
    populateRating()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()