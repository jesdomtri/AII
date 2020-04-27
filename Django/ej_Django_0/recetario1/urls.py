"""recetario1 URL Configuration


"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views import static
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<path>', static.serve,
            {'document_root': settings.MEDIA_ROOT,}),
    path('sobre/',views.sobre),
    path('usuarios/', views.usuarios),
    path('recetas/', views.lista_recetas),
    path('recetas/receta/<int:id_receta>',views.detalle_receta),
    path('',views.inicio),
    ]
