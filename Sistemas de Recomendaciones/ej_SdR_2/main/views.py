import shelve
from main.models import Book, Rating
from main.forms import UserForm, IsbnForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from main.populate import populateDatabase
from django.db.models import Avg


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat
def loadDict():
    Prefs = {}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = ra.user
        itemid = ra.isbn
        rating = ra.rating
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()


#  CONJUNTO DE VISTAS

def index(request):
    return render(request, 'index.html')


def populateDB(request):
    populateDatabase()
    return render(request, 'populate.html')


def loadRS(request):
    loadDict()
    return render(request, 'loadRS.html')


def search(request):
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            #user = get_object_or_404(UserInformation, pk=idUser)
            rating = Rating.objects.filter(user=idUser)
            libros = Book.objects.all()
            return render(request, 'ratedBooks.html', {'idUser': idUser, 'puntuaciones': rating, 'libros': libros})
    form = UserForm()
    return render(request, 'search_user.html', {'form': form})



def mejoreslibros(request):
    puntuaciones = Rating.objects.values('isbn').annotate(avg_punt=Avg('rating')).order_by('-rating')[:3]
    libros = []
    for p in puntuaciones:
        for l in Book.objects.all():
            if p["isbn"] == l.isbn:
                libros.append(l)
    return render(request, 'mejoreslibros.html', {'puntuaciones': puntuaciones, 'libros': libros})


def similarBooks(request):
    book = None
    if request.method == 'GET':
        form = IsbnForm(request.GET, request.FILES)
        if form.is_valid():
            idBook = form.cleaned_data['id']
            book = get_object_or_404(Book, isbn=idBook)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idBook), n=5)
            books = []
            similar = []
            for re in recommended:
                books.append(Book.objects.get(isbn=re[1]))
                similar.append(re[0])
            items = zip(books, similar)
            return render(request, 'similarBooks.html', {'book': book, 'books': items})
    form = IsbnForm()
    return render(request, 'search_book.html', {'form': form})


def recommendedBooksUser(request):
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = Rating.objects.filter(user=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs, int(idUser))
            recommended = rankings[:10]
            print("\n")
            print(recommended)
            print("\n")
            books = []
            scores = []
            for re in recommended:
                print("\n")
                print(re)
                print("\n")
                books.append(Book.objects.get(pk=re[1]))
                scores.append(re[0])
            items = zip(books, scores)
            return render(request, 'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request, 'search_user.html', {'form': form})
