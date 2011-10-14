from django.db import models

# Create your models here.

#Party
class Party(models.Model):
    name = models.CharField(max_length=25)
    money = models.IntegerField()
    pace = models.FloatField() 
    rations = models.FloatField()
    def __unicode__(self):
        return self.name+ u'; money:' + unicode(str(self.money))
#Profession    
class Profession(models.Model):
    name = models.CharField(max_length=25)
    def __unicode__(self):
        return self.name
    
    
#Character
class Character(models.Model):
    name = models.CharField(max_length=25)
    profession = models.CharField(max_length=25) #models.ForeignKey(Profession)
    status = models.IntegerField()
    health = models.IntegerField()
    isLeader = models.BooleanField()
    party = models.ForeignKey(Party)
    def __unicode__(self):
        return self.name+ u;'profession:'+self.profession+u'; party:'+self.party

#store
class Store(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=25)
    max_capacity = models.IntegerField()
    capacity = models.IntegerField()
    isVendor = models.BooleanField()
    price_mult = models.FloatField()
    def __unicode__(self):
        return self.name +u'; cap:' +unicode(str(self.capacity))+ u';'
    
#item
class BaseItem(models.Model):
    name = models.CharField(max_length=25)
    #store = models.ForeignKey(Store)
    #amount = models.IntegerField()
    baseCost = models.IntegerField()
    desc = models.CharField(max_length=500)
    weight = models.IntegerField()
    def __unicode__(self):
        return  self.name + u'; cost:' + unicode(self.baseCost) + u'; wt:' + unicode(self.weight)
    
class Item(models.Model):
    base = models.ForeignKey(BaseItem)
    store = models.ForeignKey(Store)
    amount = models.IntegerField()
    def __unicode__(self):
        return self.base + u'; inStore:' + self.store + u'; amount:' + unicode(self.amount)
    
#wagon
class Wagon(models.Model):
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store)
    weight = models.FloatField()
    def __unicode__(self):
        return self.party + u'; inven:' + self.inventory + u'; totalWeight:' + unicode(self.weight)

#Location
class Location(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=500)
    def __unicode__(self):
        return self.name
    
#Event
class Event(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    location = models.ForeignKey(Location)
    def __unicode__(self):
        return self.name