from models import *


#wagon = Wagon(partyz)Wo
#wagon.save()



            

#def storeLoader(storeid):
#    """
#    The initializer for the initial store in the game.
#    @param storeid the id of the store. if attached to location
#    @return an object of the store just loaded. can be modified and .save()'d
#    """
#    astore = Store.objects.get(id=storeid)
#    return astore;
def takeATurn(partyid):
    party = Party.objects.get(id = partyid)
    party.consumeFood()
    moveLocation(partyid)
    
def buyItem(partyid, itemName, num, mult): # string, string, int, float
    """
    @param item: the item to buy 
    @param amount: amount the user wants
    Buys an items
    Checks for sufficient money and capacity
    @return: String: string based on the success of the transaction
    """
    msg = "Your transaction was successful."
    # creating an item here
    abase = Item.objects.get(name=itemName)
    party = Party.objects.get(id = partyid)
    wag = party.wagon_set.all()[0]
    if wag.checkWagCap(abase, num):
        if (wag.party.money - (mult * abase.baseCost * num)) >= 0:
            wag.party.money -= mult * abase.baseCost * num
            wag.party.save()
            wag.weight += abase.weight * num
            if not wag.inventory.hasItem(itemName):
                newItem = Iteminstance(Item.objects.get(name=itemName),num,wag.inventory)
                newItem.save()
            else:
                thing = wag.inventory.iteminstance_set.get(base = abase)
                thing.amount += num
                thing.save()
            wag.save()
        else:
            msg = "You do not have enough money for this purchase."
    else:
        msg = "Your wagon cannot carry this much weight"
        if wag.party.money - item.calculatePrice() >= 0:
            msg += "and you do not have enough money for this purchase."
        else:
            msg += "."
    return msg


def moveLocation(partyid): #int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else)
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
 

    party = Party.objects.get(id=partyid)
    party.location+=int(party.pace/.5)
    party.save()
    """
    numSpaces = party.pace/6.25 # (each index is 6.25 miles)
    place = locmap[party.location] # a Location
    for x in range(1, int(numSpaces+1)):
        party.location += 1
        place = locmap[party.location] # a Location
        if place.halt:
            break
    party.save()
    place.do() 
    """
    return
    
    
def getFood(partyid):
    """
    @param wagon: takes in a wagon to access the player's inventory
    This is used to find out how much Food we have at any given point.
    @return: the amount of rations the player currently has left 
    """
    party = Party.objects.get(id=partyid)
    wagon = party.wagon_set.all()[0]
    for thing in wagon.inventory.items.all():
        if thing.name == "Food":
            return thing.amount
    return 0


#def populateLocations():
#    """
#    This generates the map, which is represented as a list of Locations
#    @return: A list of Locations
#    """
#    locations=[]
#    events = []
#    for x in range(131):
#        loc = Location()
#        locations.append(loc)
#        events.append(Event(location = loc))
#    locations[0] = Location(name = "Hobbiton",halt=True)
#    events[0] = StoreEvent()
#    locations[16] = Location(name = "Bree",halt=True)
#    events[16] = StoreEvent()
#    locations[48] = Location(name = "Thrabad",halt=True)
#    events[48] = StoreEvent()
#    locations[100] = Location(name = "Gap of Rohan",halt=True)
#    events[100] = StoreEvent()
#    locations[120] = Location(name = "Edoras",halt=True)
#    events[120] = StoreEvent()
#    locations[160] = Location(name = "Minas Tirith",halt=True)
#    events[160] = StoreEvent()
#    locations[177] = Location(name = "Mordor",halt=True)
#    events[177] = EndGame()
#    
#    for x in locations:
#        x.save()
#    for y in events:
#        y.save()    
        
