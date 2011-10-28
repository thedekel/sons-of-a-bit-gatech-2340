from models import *



#wagon = Wagon(partyz)
#wagon.save()

#for article in itemDict:
#    newItem  = Item(article[0], article[1], article[2], store, maxAmounts, article[3])
#    newItem.save()
#    wagon.inventory.addItem(newItem) # puts item holder in inventory at 0 amount

def populateLocations():
    """
    This generates the map, which is represented as a list of Locations
    @return: A list of Locations
    """
    locations=[]
    for x in range(50):
        locations[x] = Location()
    location[25] = Location(name = "Mines of Moria")
    location[49] = Location(name = "Mordor")
    return locations
    
def storeMaker(storeName, maxAmounts, bannedItems):
    """
    The initializer for the initial store in the game.
    @param storeName: The name of the store. string
    @param maxAmounts: How much of each item does this store carry? int
    @param bannedItems: What items is this store missing?  list
    """
    astore = Store(name = storeName)
    astore.save()
    for i in range(len(itemDict)):
       # if article not in bannedItems:
        article = itemDict[i]
        Item(name=article[0], description=article[1], baseCost= article[2], store=astore, amount = maxAmounts, weight = article[3]).save()
        print article
        print itemDict
#            astore.addItem(newItem)
    return astore;
        

def moveLocation(map, currentLocation, numSpaces): #array of Locations, int, int
    """
    Moves along the map array to "change" location.
    Any locations that would force a halt will be checked for here (representing with a boolean field in Location, will change later to something else).
    Most of these parameters probably won't be needed
    -Anthony Taormina
    """
    numSpaces *= 2 # (each index is .5 km)
    for x in range(1, numSpaces+1):
        place = map[currentLocation + x] # a Location
        if place.halt:
            break
    place.do()
    
    
    
