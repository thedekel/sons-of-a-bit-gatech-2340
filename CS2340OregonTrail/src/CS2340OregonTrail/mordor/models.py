from django.db import models

# Create your models here.

#Party
class Party(models.Model):
    name = models.CharField(max_length=25)
    money = models.IntegerField()
    
#Profession    
class Profession(models.Model):
    name = models.CharField(max_length=25)
    
#Character
class Character(models.Model):
    name = models.CharField(max_length=25)
    profession = models.ForeignKey(Profession)
    status = models.IntegerField()
    health = models.IntegerField()
    isLeader = models.BooleanField()
    party = models.ForeignKey(Party)

#store
class Store(models.Model):
    name = models.CharField(max_length=25)
    max_capacity = models.IntegerField()
    capacity = models.IntegerField()
    isVendor = models.BooleanField()
    price_mult = models.FloatField()
    
#item
class Item(models.Model):
    name = models.CharField(max_length=25)
    store = models.ForeignKey(Store)
    amount = models.IntegerField()
    baseCost = models.IntegerField()
    desc = models.CharField(max_length=500)
    weight = models.IntegerField()
    
#wagon
class Wagon(models.Model):
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store)
    weight = models.FloatField()

#Location
class Location(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=500)
    
#Event
class Event(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    location = models.ForeignKey(Location)
