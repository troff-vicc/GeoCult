from django.db import models


class MyModel(models.Model):
    idTg = models.CharField(max_length=100)
    
    
class Pos(models.Model):
    posX = models.CharField(max_length=100)
    posY = models.CharField(max_length=100)
    idPlace = models.CharField(max_length=100)
    idUser = models.CharField(max_length=100)
    
    
class Buy(models.Model):
    idBuy = models.CharField(max_length=100)
    idUser = models.CharField(max_length=100)
