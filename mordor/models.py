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
    pace = models.FloatField() 
    rations = models.FloatField()
    location = models.IntegerField(default=0)
    
    def numAlive(self):
        """
        This function checks to see how many of the group members are still alive
        @return: The number of alive group members
        """
        num = 0
        for person in self.character_set.all():
            if not person.checkIfDead():
                num += 1
        return num

    def consumeFood(self):
        """
        Attempts to consume a user determined amount of Food.
        @return: boolean: True upon a successful consumption and False upon a failure.
        """
        wag = self.wagon_set.all()[0]
        return wag.inventory.removeItem("Food",self.rations*numAlive)
                
    
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
    profession = models.CharField(max_length=25)
    status = models.IntegerField() # what the hell is this for???
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
        """
        if self.health == 0:
            return True
        else:
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
        return u'<Item; Base:'# + self.name + u'; cost:' + unicode(self.baseCost)+u' >'
    

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
    
    def removeItem(self, itemName, num): # string, int
        """
        @param itemName: the name of the item to remove
        @param num: the AMOUNT to be removed 
        Removes a set number of items from a store.
        @return: boolean: In the case of more things being removed than exist, it will return False.
        Returns True on a successful removal.
        """
        ret = False
        for thing in self.iteminstance_set.all():
            if thing.base.name == itemName and thing.amount >= num:
                thing.amount -= num
                thing.save()
                ret = True
        self.save()
        return ret
        

    def hasItem(self, itemName):    #string
        """
        @param item: the item to check existence for
        Checks whether the store has the item at all
        @return: boolean: True if item exists in the Store false otherwise.
        """
        for thing in self.iteminstance_set.all():
            if thing.base.name == itemName:
                return True
        return False
    
class Iteminstance(models.Model):
    base = models.ForeignKey(Item)
    amount = models.IntegerField(default = 1)
    inventory = models.ForeignKey(Store)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Iteminstance
        """
        return u'<Iteminstance; Base:'# + unicode(self.base.name) + u' >'
    



   
    
class Wagon(models.Model):
    """
    Wagon
    """
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store, default=Store(name="Wagon", isVendor=False))
    weight = models.FloatField(default = 0)
    capacity = 1500
    
    def __unicode__(self):
        """
        @return: String: String representation of a Wagon
        """
        return u'<Wagon; Party:' + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    def checkWagCap(self, base, amountOfStuff): # item, int
        """
        @param item: the item to be added to the wagon 
        Checks to see if the added item exceeds the wagons capacity
        @return: boolean: True if adding the item does not exceed wagon capacity; false otherwise.
        """
        if self.capacity < base.weight * amountOfStuff + self.weight:
            return False
        else:
            return True
    
    
   

class Location(models.Model):
    """
    Location
    """
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    halt = models.BooleanField(default=False) # used only for moveLocation.  Will probably be implemented in a different manner -A
    x = models.IntegerField()
    y = models.IntegerField()
    index = models.IntegerField()
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
    """
    River Crossing Event
    """
    name = "River"
    waterdepth = models.IntegerField(default = 2)
    ferryfee = models.IntegerField(default = 250)
    
    def takeFerry(self, partyid): #string
        """
        Takes the Ferry. Takes a designated amount of money away from the player
        to use the ferry
        """
        party.money -= self.ferryfee
    
    def ford(self):
        """
        Attempts to ford the river. Fails if water depth is greater than 3 feet.
        @return: String: The success or failure of fording the river
        """
        chance = random.randint(0,100)
        percentChance = 5 * self.waterdepth
        if (chance > (100 - percentChance)):
            msg = "DUDE FLIP THE WAGON!"
    
    def caulk(self):
        """
        Attempts to float over the river on the wagon. Greater chance of wagon flip.
        @return: String: The success or failure of caulking the river
        """
        chance = random.randint(0,100)
        if (chance > 70):
            msg = "DUDE FLIP THE WAGON"
    
    def do(self):
        return
    
class StoreEvent(Event):
    name = "Store"
    def do(self):
        return
    

class EndGame(Event):
    def do(self):
        return
