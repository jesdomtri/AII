#encoding:utf-8
from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Autor')

    def __str__(self):
        return self.nombre
    
class Fuente(models.Model):
    nombre = models.CharField(max_length=30,verbose_name='Fuente')

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.TextField(verbose_name='Título')
    autor = models.ForeignKey(Autor,on_delete=models.SET_NULL, null=True)
    fuente = models.ForeignKey(Fuente,on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(verbose_name='Fecha y hora')
    contenido = models.TextField(verbose_name="Contenido")
    num_comentarios = models.IntegerField(verbose_name='Número de comentarios')
    
    def __str__(self):
        return self.titulo
    