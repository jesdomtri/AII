#encoding:utf-8
from django.db import models

class Bodega(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Bodega')

    def __str__(self):
        return self.nombre
    
class Denominacion(models.Model):
    nombre = models.CharField(max_length=30,verbose_name='Denominación')

    def __str__(self):
        return self.nombre

class Uva(models.Model):
    nombre = models.CharField(max_length=30,verbose_name='Uva')

    def __str__(self):
        return self.nombre

class Vino(models.Model):
    nombre = models.CharField(max_length=120,verbose_name='Nombre')
    bodega = models.ForeignKey(Bodega,on_delete=models.SET_NULL, null=True)
    denominacion = models.ForeignKey(Denominacion,on_delete=models.SET_NULL, null=True)
    uva = models.ManyToManyField(Uva)
    precio = models.FloatField(verbose_name='Precio')
    puntuacion = models.FloatField(verbose_name='Puntuacion', null=True)

    
    def __str__(self):
        return self.nombre
    