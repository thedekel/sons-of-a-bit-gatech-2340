from django.db import models

# Create your models here.
"""
Party
"""
class Party(models.Model):
    name = models.CharField(max_length=25)
    money = models.IntegerField()
    pace = models.IntegerField() 
    rations = models.IntegerField()
    
    def consumeFood(self, rationNum):
        """
        Attempts to consume a user determined amount of food.
        Returns True upon a successful consumption and False upon a failure.
        """
        if self.rations >= rationNum:
            self.rations -= rationNum
            return True
        else:
            return False
    
    """
    String representation of a Party
    """
    def __unicode__(self):
        return u'<Party:'+self.name+ u'; money:' + unicode(str(self.money))+u' >'
"""
Profession    
"""
class Profession(models.Model):
    name = models.CharField(max_length=25)
    
    """
    String representation of a Profession
    """
    def __unicode__(self):
        return u'<Profession:'+self.name+u' >'
    
    
"""
Character
"""
class Character(models.Model):
    name = models.CharField(max_length=25)
    profession = models.CharField(max_length=25) #models.ForeignKey(Profession)
    status = models.IntegerField()
    health = models.IntegerField()
    isLeader = models.BooleanField()
    party = models.ForeignKey(Party)
    
    """
    String representation of a Character
    """
    def __unicode__(self):
        return u'<Name: '+ self.name+u'; profession:'+unicode(self.profession)+u'; party:'+unicode(self.party) + u' >'

"""
Store
"""
class Store(models.Model):
    store_id = models.IntegerField()
    name = models.CharField(max_length=25)
    isVendor = models.BooleanField(default=True)
    price_mult = models.FloatField()
    
    """
    String representation of a Store
    """
    def __unicode__(self):
        return u'<Store:'+self.name +u'; capacity:' +unicode(str(self.capacity))+ u' >'
    
    """
    Adds an item 
    Returns none if item not found in store
    """
    def addItem(self, item):
        if not hasItem(item):
            item.store = self
        else:
            for thing in self.item_set.all():
                if thing.base.name == item.base.name:
                    thing.amount += item.amount
    
    def removeItem(self, itemName, num):
        """
        This will remove a set number of items from a store.
        In the case of more things being removed then present, it will return False.
        True will return on a successful removal.
        """
        for thing in self.item_set.all():
            if thing.base.name == itemName:
                if thing.amount >= item.amount:
                    thing.amount -= item.amount
                    return True
                else:
                    return False
        return False
        
    """
    Checks whether the store has a certain AMOUNT of an item
    returns a boolean
    """
    def hasItem(self, item): # takes in an Item
        for thing in self.item_set.all():
            if thing.base.name == item.base.name:
                if thing.amount >= item.amount:
                    return True
                else:
                    return False
        return False
    
"""
Base Item
"""
class BaseItem(models.Model):
    name = models.CharField(max_length=25)
    #store = models.ForeignKey(Store)
    #amount = models.IntegerField()
    baseCost = models.IntegerField()
    desc = models.CharField(max_length=500)
    weight = models.IntegerField()
    
    """
    String representation of a BaseItem
    """
    def __unicode__(self):
        return  u'<BaseItem:'+self.name + u'; cost:' + unicode(self.baseCost) + u'; weight:' + unicode(self.weight)+u' >'
    
class Item(models.Model):
    base = models.ForeignKey(BaseItem)
    store = models.ForeignKey(Store)
    amount = models.IntegerField()
    
    """
    String representation of a Item
    """
    def __unicode__(self):
        return u'<Item; Base:' + self.base + u'; inStore:' + unicode(self.store) + u'; amount:' + unicode(self.amount)+u' >'
    
    """
    Calculates the price of a given item based of it's base item price and store multiplier
    returns a float
    """
    def calculatePrice(self): # NOT per item
        return store.price_mult * base.baseCost * amount 
    
"""
Wagon
"""
class Wagon(models.Model):
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store)
    inventory.isVendor = False
    weight = models.FloatField(default = 0)
    capacity = 1500 # CHANGE THIS LATER or not
    
    """
    String representation of a Wagon
    """
    def __unicode__(self):
        return u'<Wagon; Party:' + self.party + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    """
    Checks to see if the added item exceeds the wagons capacity
    returns a boolean
    """
    def checkWagCap(self, item): #item must be an Item 
        if capacity < item.base.weight * item.amount + self.weight:
            return False
        else:
            return True
    
    
    def buyItem(self, item): #item must be an Item
        """
        Buys an items
        Has checks for money and capacity
        returns a string based on the success of the transaction
        """
        msg = "Your transaction was successful."
        if self.checkWagCap(item):
            if self.party.money - item.calculatePrice() >= 0:
                self.party.money -= item.calculatePrice()
                self.weight += item.base.weight * item.amount
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
    

"""
Location
"""
class Location(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=500)
    #halt = models.BooleanField(default=False) used only for moveLocation.  Will probably be implemented in a different manner -AT
    
    """
    String representation of a Location
    """
    def __unicode__(self):
        return u'<Location: '+self.name+u' >'
    
     #==========================================================================
     # def moveLocation(map, currentLocation, numSpaces): #array of Locations, int, int
     #   """
     #   Moves along the map array to "change" location.
     #   Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else).
     #   Most of these parameters probably won't be needed
     #   -Anthony Taormina
     #   """
     #   numSpaces *= 2 # (each index is .5 km)
     #   for x in range(1, numSpaces+1):
     #       place = map[currentLocation + x] # a Location
     #       if place.halt:
     #           # Do stuff? We stop things here
     #       else:
     #           # ???
     #==========================================================================
    
     
"""
Event
"""
class Event(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    location = models.ForeignKey(Location)
    
    """
    String representation of a Event
    """
    def __unicode__(self):
        return u'<Event' + self.name + u' >'

 
