from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator


class Rating(models.Model):
    user = models.IntegerField()
    animeid = models.IntegerField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    def __str__(self):
        return str(self.user) + "/" + str(self.animeid) + "/" +  str(self.rating)  

class Anime(models.Model):
    animeid = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    generos = models.TextField(verbose_name='generos')
    formato = models.CharField(max_length=100)
    numepisodios = models.CharField(max_length=100)
    def __str__(self):
        return str(self.animeid)