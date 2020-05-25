from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator


class Rating(models.Model):
    user = models.IntegerField()
    isbn = models.IntegerField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    def __str__(self):
        return str(self.isbn) + "/" +  str(self.rating)  

class Book(models.Model):
    isbn = models.IntegerField()
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    anyo = models.CharField(max_length=100)
    editor = models.CharField(max_length=100)
    def __str__(self):
        return str(self.isbn) + "/" + self.titulo

    
