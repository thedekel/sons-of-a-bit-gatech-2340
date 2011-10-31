from django.db import models
from random import *

"""
@author: Alex Williams, Anthony Taormina, Daniel Whatley, Stephen Roca, Yuval Dekel
"""

# Create your models here.
class Party(models.Model):
    """
    Party
    """
    name = models.CharField(max_length=25)
    money = models.IntegerField()
    pace = models.IntegerField() 
    rations = models.IntegerField()
    location = models.IntegerField(default=0)
    
    def consumeFood(self, wag):
        """
        Attempts to consume a user determined amount of food.
        @return: boolean: True upon a successful consumption and False upon a failure.
        """
        return wag.inventory.removeItem("food",self.rations)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Party
        """
        return u'<Party:'+self.name+ u'; money:' + unicode(str(self.money))+u' >'
    
    
class Profession(models.Model):
    """
    Profession    
    """
    name = models.CharField(max_length=25)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Profession
        """
        return u'<Profession:'+self.name+u' >'
    
    

class Character(models.Model):
    """
    Character
    """
    name = models.CharField(max_length=25)
    profession = models.CharField(max_length=25) #models.ForeignKey(Profession)
    status = models.IntegerField()
    health = models.IntegerField()
    isLeader = models.BooleanField()
    party = models.ForeignKey(Party)
    

    def __unicode__(self):
        """
        @return: String: String representation of a Character
        """
        return u'<Name: '+ self.name+u'; profession:'+unicode(self.profession)+u'; party:'+unicode(self.party) + u' >'

    def checkIfDead(self):
        """
        Checks to see whether a player is dead or not
        @return: boolean: True if player is dead. False otherwise.
        if self.health == 0
            return True
        else
            return False
   
class Item(models.Model):
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    baseCost = models.IntegerField(default = 10)
    weight = models.IntegerField(default = 10)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Item
        """
        return u'<Item; Base:' + self.name + u'; cost:' + unicode(self.baseCost)+u' >'
    

class Store(models.Model):
    """
    Store
    """
    name = models.CharField(max_length=25, default = "")
    items = models.ManyToManyField(Item)
    isVendor = models.BooleanField(default=True)
    price_mult = models.FloatField(default = 1)
    location = models.IntegerField(default = -1)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Store
        """
        return u'<Store:'+self.name +u' >'
    

    def addItem(self, item): #iteminstance
        """
        @param item: the iteminstance to add 
        Adds the item given in as a parameter
        """
        if not self.hasItem(item):
            item.inventory = self
            item.save()
        else:
            for thing in self.items_set.all():
                if thing.base.name == item.base.name:
                    thing.amount += item.amount
                    thing.save()
        self.save()
    
    def removeItem(self, itemName, num): # string, int
        """
        @param itemName: the name of the item to remove
        @param num: the AMOUNT to be removed 
        Removes a set number of items from a store.
        @return: boolean: In the case of more things being removed than exist, it will return False.
        Returns True on a successful removal.
        """
        for thing in self.items_set.all():
            if thing.base.name == itemName:
                if thing.amount >= item.amount:
                    thing.amount -= item.amount
                    thing.save()
                    ret = True
                else:
                    ret = False
        self.save()
        return ret
        

    def hasItem(self, item):    #iteminstance
        """
        @param item: the item to check existence for
        Checks whether the store has a certain AMOUNT of an ite
        @return: boolean: True if item exists in the Store false otherwise.
        """
        for thing in self.items_set.all():
            if thing.base.name == item.base.name:
                if thing.amount > 0:
                    return True
                else:
                    return False
    
class Iteminstance(models.Model):
    base = models.ForeignKey(Item)
    amount = models.IntegerField(default = 1)
    inventory = models.ForeignKey(Store)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Iteminstance
        """
        return u'<Iteminstance; Base:' + unicode(self.item) + ' >'
    
    def calculatePrice(self): # per item
        """
        Calculates the price of a given item based of it's base item price and store multiplier
        @return: float: the price of the individual item multiplied by the store multiplier
        """
        return self.store.price_mult * self.base.baseCost



   
    
class Wagon(models.Model):
    """
    Wagon
    """
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store, default=Store(name="Wagon", isVendor=False))
    weight = models.FloatField(default = 0)
    capacity = 1500 # CHANGE THIS LATER or not
    
    def __unicode__(self):
        """
        @return: String: String representation of a Wagon
        """
        return u'<Wagon; Party:' + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    def checkWagCap(self, item): # iteminstance
        """
        @param item: the item to be added to the wagon 
        Checks to see if the added item exceeds the wagons capacity
        @return: boolean: True if adding the item does not exceed wagon capacity; false otherwise.
        """
        if self.capacity < item.base.weight * item.amount + self.weight:
            return False
        else:
            return True
    
    
    def buyItem(self, itemName, amountOfStuff): # string, int
        """
        @param item: the item to buy 
        @param amount: amount the user wants
        Buys an items
        Checks for sufficient money and capacity
        @return: String: string based on the success of the transaction
        """
        msg = "Your transaction was successful."
        # creating an iteminstance here
#        for x in itemList:
#            if x[0] == itemName:
#                item =  Item(name=x[0], description=x[1], baseCost= x[2], store=dummyStore, amount = amountOfStuff, weight = x[3])
#                item.save()
        if self.checkWagCap(item):
            if (self.party.money - (item.calculatePrice() * item.amount)) >= 0:
                self.party.money -= item.calculatePrice() * item.amount
                self.party.save()
                self.weight += item.base.weight * item.amount
                self.inventory.addItem(item)
                self.save()
            else:
                msg = "You do not have enough money for this purchase."
        else:
            msg = "Your wagon cannot carry this much weight"
            if self.party.money - item.calculatePrice() >= 0:
                msg += "and you do not have enough money for this purchase."
            else:
                msg += "."
        return msg
    

class Location(models.Model):
    """
    Location
    """
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    halt = models.BooleanField(default=False) # used only for moveLocation.  Will probably be implemented in a different manner -A
    
    def __unicode__(self):
        """
        @return: String: String representation of a Location
        """
        return u'<Location: u>'
    

    
class Event(models.Model):
    """
    Event
    """
    name = models.CharField(max_length=25)
    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Event
        """
        return u'<Event' + self.name + u' >'
    
    def do(self):
        return
    
class RiverCrossingEvent(Event):
    #TODO
    name = "River"
    waterdepth = models.IntegerField(default = 2)
    
    def takeFerry(self, party): #Party
        party.money -= 25
        return
    
    def ford(self):
        chance = random.randint(0,100)
        percentChance = 5 * self.waterdepth
        if (chance > (100 - percentChance))
            msg = "DUDE FLIP THE WAGON!"
        else
        return
    
    def caulk(self):
        chance = random.randint(0,100)
        if (chance > 70)
            msg = "DUDE FLIP THE WAGON"
        else
        return
    #DEFINE DO!
    
class StoreEvent(Event):
    name = "Store"
    def do(self):
        return
    
itemList = [ # this is where you add items to the game (name, description, basecost, weight)
            ("Food", "This is edible stuff.", 1, 1),
            ("Wagon Wheel", "don't eat it. use it for wagon!", 100, 10)
            ]
dummyStore = Store()
