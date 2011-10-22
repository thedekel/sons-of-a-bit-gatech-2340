from django.db import models

# Create your models here.

#Party
class Party(models.Model):
    name = models.CharField(max_length=25)
    money = models.IntegerField()
    pace = models.FloatField() 
    rations = models.FloatField()
    
    def __unicode__(self):
        return u'<Party:'+self.name+ u'; money:' + unicode(str(self.money))+u' >'
    
#Profession    
class Profession(models.Model):
    name = models.CharField(max_length=25)
    
    def __unicode__(self):
        return u'<Professoin:'+self.name+u' >'
    
    
#Character
class Character(models.Model):
    name = models.CharField(max_length=25)
    profession = models.CharField(max_length=25) #models.ForeignKey(Profession)
    status = models.IntegerField()
    health = models.IntegerField()
    isLeader = models.BooleanField()
    party = models.ForeignKey(Party)
    
    def __unicode__(self):
        return u'<Name: '+ self.name+u'; profession:'+unicode(self.profession)+u'; party:'+unicode(self.party) + u' >'

#store
class Store(models.Model):
    store_id = models.IntegerField()
    name = models.CharField(max_length=25)
    max_capacity = models.IntegerField()
    capacity = models.IntegerField()
    isVendor = models.BooleanField()
    price_mult = models.FloatField()
    
    def __unicode__(self):
        return u'<Store:'+self.name +u'; capacity:' +unicode(str(self.capacity))+ u' >'
    
    def addItem(self, item, num):
        #TODO
        return None
        
    def hasItem(self, item):
        #TODO
        return None
    
#item
class BaseItem(models.Model):
    name = models.CharField(max_length=25)
    #store = models.ForeignKey(Store)
    #amount = models.IntegerField()
    baseCost = models.IntegerField()
    desc = models.CharField(max_length=500)
    weight = models.IntegerField()
    
    def __unicode__(self):
        return  u'<BaseItem:'+self.name + u'; cost:' + unicode(self.baseCost) + u'; weightt:' + unicode(self.weight)+u' >'
    
class Item(models.Model):
    base = models.ForeignKey(BaseItem)
    store = models.ForeignKey(Store)
    amount = models.IntegerField()
    
    def __unicode__(self):
        return u'<Item; Base:' + self.base + u'; inStore:' + unicode(self.store) + u'; amount:' + unicode(self.amount)+u' >'
    
    def calcultatePrice(self):
        #TODO
        return None
    
#wagon
class Wagon(models.Model):
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store)
    weight = models.FloatField()
    
    def __unicode__(self):
        return u'<Wagon; Party:' + self.party + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    def checkWagCap(self, item):
        #TODO
        return None
    
    def buyItem(self, item, num):
        if self.checkWagCap(item):
            self.inventory.
        
        
        #TODO
        return None
    

#Location
class Location(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=500)
    
    def __unicode__(self):
        return u'<Location: '+self.name+u' >'
    
#Event
class Event(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        return u'<Event' + self.name + u' >'