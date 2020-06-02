import shelve
from main.models import Anime, Rating
from main.forms import UserForm, BusquedaPorGeneroForm
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
        itemid = ra.animeid
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
    animes = Anime.objects.all().count()
    puntuaciones = Rating.objects.all().count()
    return render(request, 'populate.html', {'animes': animes, 'puntuaciones': puntuaciones})


def loadRS(request):
    loadDict()
    return render(request, 'loadRS.html')


def puntuacionesUsuarios(request):
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            rating = Rating.objects.filter(user=idUser)
            animes = Anime.objects.all()
            return render(request, 'ratedAnimes.html', {'idUser': idUser, 'puntuaciones': rating, 'animes': animes})
    form = UserForm()
    return render(request, 'search_user.html', {'form': form})

def animesGeneros(request):
    formulario = BusquedaPorGeneroForm()
    animes = []
    if request.method=='POST':
        formulario = BusquedaPorGeneroForm(request.POST)
        if formulario.is_valid():
            for anime in Anime.objects.all():
                if formulario.cleaned_data['genero'] in anime.generos:
                    animes.append(anime)
    return render(request, 'busquedaporgenero.html', {'formulario':formulario, 'animes':animes})


def usuariosParecidos(request):
    punt = None
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            punt = Rating.objects.filter(user=idUser)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['Prefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idUser), n=3)
            users = []
            similar = []
            for re in recommended:
                users.append(Rating.objects.filter(user=re[1]).first())
                similar.append(re[0])
            items = zip(users, similar)
            return render(request, 'similarUsers.html', {'idUser':idUser,'punt': punt, 'users': items})
    form = UserForm()
    return render(request, 'search_user.html', {'form': form})


def animesRecomendados(request):
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = Rating.objects.filter(user=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:5]
            animes = []
            scores = []
            for re in recommended:
                animes.append(Anime.objects.get(animeid=re[1]))
                scores.append(re[0])
            items = zip(animes, scores)
            animes = Anime.objects.all()
            return render(request, 'recommendationItems.html', {'user': user, 'items': items, 'animes':animes})
    form = UserForm()
    return render(request, 'search_user.html', {'form': form})