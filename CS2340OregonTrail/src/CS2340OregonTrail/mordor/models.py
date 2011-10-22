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
        return u'<Profession:'+self.name+u' >'
    
    
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
    isVendor = models.BooleanField(default=True)
    price_mult = models.FloatField()
    
    def __unicode__(self):
        return u'<Store:'+self.name +u'; capacity:' +unicode(str(self.capacity))+ u' >'
    
    def addItem(self, item):
        if !hasItem(item):
            item.store = self
        else:
            pass
        return None
        
    def hasItem(self, item): # takes in an Item
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
        return  u'<BaseItem:'+self.name + u'; cost:' + unicode(self.baseCost) + u'; weight:' + unicode(self.weight)+u' >'
    
class Item(models.Model):
    base = models.ForeignKey(BaseItem)
    store = models.ForeignKey(Store)
    amount = models.IntegerField()
    
    def __unicode__(self):
        return u'<Item; Base:' + self.base + u'; inStore:' + unicode(self.store) + u'; amount:' + unicode(self.amount)+u' >'
    
    def calculatePrice(self): # NOT per item
        return store.price_mult * base.baseCost * amount 
    
#wagon
class Wagon(models.Model):
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store)
    inventory.isVendor = False
    weight = models.FloatField(default = 0)
    capacity = 1500 # CHANGE THIS LATER or not
    
    def __unicode__(self):
        return u'<Wagon; Party:' + self.party + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    def checkWagCap(self, item): #item must be an Item 
        if capacity < item.base.weight * item.amount + self.weight:
            return False
        else:
            return True
    
    def buyItem(self, item): #item must be an Item
        msg = "Your transaction was successful."
        if self.checkWagCap(item):
            if self.party.money - item.calculatePrice() >= 0:
                self.party.money -= item.calculatePrice()
                self.inventory.addItem(item)
            else:
                msg = "You do not have enough money for this purchase."
        else:
            msg = "Your wagon cannot carry this much weight"
            if self.party.money - item.calculatePrice() >= 0:
                msg += "and you do not have enough money for this purchase."
            else:
                msg += "."
        return msg
    

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