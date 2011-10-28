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
    location = models.IntegerField(default=0)
    
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
        if not self.hasItem(item):
            item.save()
            item.store = self
        else:
            for thing in self.item_set.all():
                if thing.name == item.name:
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
            if thing.name == itemName:
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
            if thing.name == item.name:
                if thing.amount > 0:
                    return True
                else:
                    return False
    
    
class Item(models.Model):
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    baseCost = models.IntegerField(default = 10)
    store = models.ForeignKey(Store)
    amount = models.IntegerField(default = 0)
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
        return self.store.price_mult * self.baseCost
    
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
        return u'<Wagon; Party:' + self.party + u'; inventory:' + unicode(self.inventory) + u'; totalWeight:' + unicode(self.weight)+u' >'
    
    def checkWagCap(self, item): #item must be an Item 
        """
        @param item: the item to be added to the wagon 
        Checks to see if the added item exceeds the wagons capacity
        @return: boolean: True if adding the item does not exceed wagon capacity; false otherwise.
        """
        if self.capacity < item.base.weight * item.amount + self.weight:
            return False
        else:
            return True
    
    
    def buyItem(self, item, amount):
        """
        @param item: the item to buy 
        @param amount: amount the user wants
        Buys an items
        Checks for sufficient money and capacity
        @return: String: string based on the success of the transaction
        """
        msg = "Your transaction was successful."
        item.amount = amount
        if self.checkWagCap(item):
            if self.party.money - item.calculatePrice() * item.amount >= 0:
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
    name = models.CharField(max_length=25, default = "")
    description = models.CharField(max_length=500, default = "")
    #halt = models.BooleanField(default=False) used only for moveLocation.  Will probably be implemented in a different manner -AT
    
    def __unicode__(self):
        """
        @return: String: String representation of a Location
        """
        return u'<Location: '+self.name+u' >'
    

    
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
    
class StoreEvent(Event):
    name = "Store"
    def do(self):
        
        return
    

 
