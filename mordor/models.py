from django.db import models
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
    
    def consumeFood(self, rationNum):
        """
        @param param: 
        Attempts to consume a user determined amount of food.
        @return: boolean: True upon a successful consumption and False upon a failure.
        """
        if self.rations >= rationNum:
            self.rations -= rationNum
            return True
        else:
            return False
    
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

class Store(models.Model):
    """
    Store
    """
    #store_id = models.IntegerField()
    name = models.CharField(max_length=25, default = "")
    isVendor = models.BooleanField(default=True)
    price_mult = models.FloatField(default = 1)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Store
        """
        return u'<Store:'+self.name +u'; capacity:' +unicode(str(self.capacity))+ u' >'
    

    def addItem(self, item):
        """
        @param item: the item to add 
        Adds the item given in as a parameter
        """
        if not hasItem(item):
            item.store = self
        else:
            for thing in self.item_set.all():
                if thing.base.name == item.base.name:
                    thing.amount += item.amount
    
    def removeItem(self, itemName, num):
        """
        @param itemName: the name of the item to remove
        @param num: the AMOUNT to be removed 
        Removes a set number of items from a store.
        @return: boolean: In the case of more things being removed than exist, it will return False.
        Returns True on a successful removal.
        """
        for thing in self.item_set.all():
            if thing.base.name == itemName:
                if thing.amount >= item.amount:
                    thing.amount -= item.amount
                    return True
                else:
                    return False
        return False
        

    def hasItem(self, item):
        """
        @param item: the item to check existence for
        Checks whether the store has a certain AMOUNT of an item
        @return: boolean: True if item exists in the Store false otherwise.
        """
        for thing in self.item_set.all():
            if thing.base.name == item.base.name:
                return True
        return False
    
    
class Item(models.Model):
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    baseCost = models.IntegerField(default = 10)
    store = models.ForeignKey(Store)
    amount = models.IntegerField(default = 1)
    weight = models.IntegerField(default = 10)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Item
        """
        return u'<Item; Base:' + self.name + u'; inStore:' + unicode(self.store) + u'; amount:' + unicode(self.amount)+u' >'
    

    def calculatePrice(self): # per item
        """
        Calculates the price of a given item based of it's base item price and store multiplier
        @return: float: the price of the individual item multiplied by the store multiplier
        """
        return store.price_mult * baseCost
    
class Wagon(models.Model):
    """
    Wagon
    """
    party = models.ForeignKey(Party)
    inventory = models.ForeignKey(Store)
    inventory.isVendor = False
    weight = models.FloatField(default = 0)
    capacity = 1500 # CHANGE THIS LATER or not
    
    def __unicode__(self):
        """
        @return: String: String representation of a Wagon
        """
        return u'<Wagon; Party:' + self.party + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    def checkWagCap(self, item): #item must be an Item 
        """
        @param item: the item to be added to the wagon 
        Checks to see if the added item exceeds the wagons capacity
        @return: boolean: True if adding the item does not exceed wagon capacity; false otherwise.
        """
        if capacity < item.base.weight * item.amount + self.weight:
            return False
        else:
            return True
    
    
    def buyItem(self, name, description, amount, cost, weight):
        """
        @param item: the item to buy 
        @param amount: amount the user wants
        Buys an items
        Checks for sufficient money and capacity
        @return: String: string based on the success of the transaction
        """
        msg = "Your transaction was successful."
        if self.checkWagCap(item):
            if self.party.money - (item.calculatePrice() * amount) >= 0:
                item.amount = amount
                self.party.money -= item.calculatePrice() * item.amount
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
    

class Location(models.Model):
    """
    Location
    """
    #type_id = models.IntegerField()
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    #halt = models.BooleanField(default=False) used only for moveLocation.  Will probably be implemented in a different manner -AT
    
    def __unicode__(self):
        """
        @return: String: String representation of a Location
        """
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
    
class Event(models.Model):
    """
    Event
    """
    type_id = models.IntegerField()
    name = models.CharField(max_length=25)
    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        """
        @return: String: String representation of a Event
        """
        return u'<Event' + self.name + u' >'

 
