#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    path('loadRS', views.loadRS),
    path('mejoreslibros/', views.mejoreslibros),
    path('search/', views.search),
    path('librosSimilares/', views.similarBooks),
    path('librosRecomendados/', views.recommendedBooksUser),
    path('admin/', admin.site.urls),
]