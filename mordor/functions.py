from models import *


#wagon = Wagon(partyz)
#wagon.save()

#for article in itemDict:
#    newItem  = Item(article[0], article[1], article[2], store, maxAmounts, article[3])
#    newItem.save()
#    wagon.inventory.addItem(newItem) # puts item holder in inventory at 0 amount

def storeMaker(aname, items, amounts):
    """
    Creates a store that will match the items and amount specified.
    @param: name, a string representation of the store, aka a name.
    @param: items, a list of item-names that will be included in the store.
    @param: amounts, either an int or a list of ints. specifies amount for all items
            or for specific items that match the index of items
    """
    if type(amonuts)==type(1):
        items = map(lambda q: [q,amounts], items)
    elif (reduce(lambda a,b: type(a) if type(a)==type(b)==type(1) else type(1.11), amounts)==type(1) and len(items)==len(amounts)):
        map(lambda a,b: [a,b], items,amonuts)
    else:
        return u'1'
    astore = Store(name = aname)
    astore.save()
    for i in items:
       a = itemDict[i[0]]
       ii = Item(name = a[0], description=a[1], baseCost = a[2], store = astore, amount = i[1], weight = a[3])
       ii.save()
    astore.save()
    return astore.id

            

def storeLoader(storeid):
    """
    The initializer for the initial store in the game.
    @param storeid the id of the store. if attached to location
    @return an object of the store just loaded. can be modified and .save()'d
    """
    astore = Store.objects.get(id=storeid)
    return astore;
        

def moveLocation(partyid, newPace=None): #array of int, int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else)
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
	
    party = Party.objects.get(id=partyid)
    party.pace = (party.pace if newPace==None else newpace)
    numSpaces = 2 * party.pace # (each index is .5 km)
    for x in range(1, numSpaces+1):
        place = locmap[currentLocation + x] # a Location
        if place.halt:
            break
    place.do()
    return currentLocation
    
    
def getFood(wagonid):
    """
    @param wagon: takes in a wagon to access the player's inventory
    This is used to find out how much food we have at any given point.
    @return: the amount of rations the player currently has left 
    """
	wagon = Wagon.objects.get(id=wagonid)
    for thing in wagon.inventory.item_set.all():
            if thing.name == "food":
                return thing.amount


def populateLocations():
    """
    This generates the map, which is represented as a list of Locations
    @return: A list of Locations
    """
    locations=[]
    for x in range(50):
        locations.append(Location())
    locations[25] = Location(name = "Mines of Moria")
    locations[49] = Location(name = "Mordor")
    return locations
 
locmap = populateLocations()
